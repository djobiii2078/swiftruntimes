import datetime
import io
import os
import sys
import uuid
from urllib.parse import unquote_plus
from PIL import Image

import boto3 
#from . import storage
#client = storage.storage.get_instance()

# Disk-based solution
#def resize_image(image_path, resized_path, w, h):
#    with Image.open(image_path) as image:
#        image.thumbnail((w,h))
#        image.save(resized_path)

# Memory-based solution
def resize_image(image_bytes, w, h):
    with Image.open(io.BytesIO(image_bytes)) as image:
        image.thumbnail((w,h))
        out = io.BytesIO()
        image.save(out, format='jpeg')
        # necessary to rewind to the beginning of the buffer
        out.seek(0)
        return out

def main(args):
 
    start = datetime.datetime.now() 
    input_bucket = args.get('object','1024.jpg') #.get('input')
    #output_bucket = event.get('bucket').get('output')
    #key = unquote_plus(event.get('object').get('key'))
    width = args.get('width',512) #.get('width')
    height = args.get('height',512) #.get('height')
    
    obj = boto3.client("s3", 
                       aws_access_key_id = "AWSKEYID",
                       aws_secret_access_key = "AWSSECRET"
                       )

    print ("Width: ", width, "/ Height: ", height, "\n")
    # UUID to handle multiple calls
    #download_path = '/tmp/{}-{}'.format(uuid.uuid4(), key)
    #upload_path = '/tmp/resized-{}'.format(key)
    #client.download(input_bucket, key, download_path)
    #resize_image(download_path, upload_path, width, height)
    #client.upload(output_bucket, key, upload_path)
    download_begin = datetime.datetime.now()
    obj.download_file(
            Filename = input_bucket,
            Bucket="swiftruntimes",
            Key=input_bucket
            )
    download_end = datetime.datetime.now() 

    process_begin = datetime.datetime.now() 
    img = Image.open(input_bucket) #client.download_stream(input_bucket, key)
    #download_end = datetime.datetime.now()

#    process_begin = datetime.datetime.now()
#    resized = resize_image(img, width, height)
#    resized_size = resized.getbuffer().nbytes
#    with img:
    img.thumbnail((width,height))
    img.save('output.jpg') 
    process_end = datetime.datetime.now()

    upload_begin = datetime.datetime.now()
    #key_name = client.upload_stream(output_bucket, key, resized)
    obj.upload_file(
            Filename = 'output.jpg',
            Bucket="swiftruntimes",
            Key='output.jpg'
            )
    upload_end = datetime.datetime.now()

    download_time = (download_end - download_begin) / datetime.timedelta(microseconds=1)
    #upload_time = (upload_end - upload_begin) / datetime.timedelta(microseconds=1)
    process_time = (process_end - process_begin) / datetime.timedelta(microseconds=1)

    final_width, final_height = img.size 
    
    return {
            'result': 'output.jpg',
            'start_time': datetime.datetime.timestamp(start),
            'download_time' : (download_end - download_begin)/datetime.timedelta(microseconds=1),
            'transform_time' : (process_end - process_begin)/datetime.timedelta(microseconds=1),
            'upload_time': (upload_end - upload_begin)/datetime.timedelta(microseconds=1),
            'total_time': (upload_end - start)/datetime.timedelta(microseconds=1)
    }

#for testing 
#comment when launching the function 
# also test with 205.jpg, 204.jpg 
print(main({'object': '1024.jpg', 'width':512, 'height': 512}))

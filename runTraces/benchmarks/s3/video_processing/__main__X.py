import ffmpeg 
import boto3 
import datetime

def main(args):

    start = datetime.datetime.now() 
    path_video = args.get('file','input.mp4')
    output_video = args.get('output','output.mp4')
    
    
    #download video from S3
    obj = boto3.client("s3", 
                       aws_access_key_id="AWSKEYID",
                       aws_secret_access_key="AWSSECRET"
                       )
    #                   ws_access_key_id=AWSKEYID, 
     #                 aws_secret_access_key=AWSSECRETKEY) 

    download_begin = datetime.datetime.now()    
    obj.download_file( 
    Filename=path_video, 
    Bucket="swiftruntimes", 
    Key=path_video
)
    download_end = datetime.datetime.now() 
    
    transform_begin = datetime.datetime.now() 
    input_file = ffmpeg.input(path_video)
    output_file = ffmpeg.output(input_file.trim(start_frame=100, end_frame=1800), output_video)


    ffmpeg.run(output_file,cmd="/usr/bin/ffmpeg",overwrite_output=True)

    transform_end = datetime.datetime.now() 

    upload_begin = datetime.datetime.now() 

    obj.upload_file(
            Filename = output_video, 
            Bucket="swiftruntimes",
            Key=output_video
            ) 

    upload_end = datetime.datetime.now() 
    
    return { 'result' : output_video, 
            'start_time': datetime.datetime.timestamp(start),
            'download_time': (download_end - download_begin)/datetime.timedelta(microseconds=1),
            'transform_time': (transform_end - transform_begin)/datetime.timedelta(microseconds=1),
            'upload_time': (upload_end - upload_begin)/datetime.timedelta(microseconds=1), 
            'total_time': (upload_end - start)/datetime.timedelta(microseconds=1)
            }


#should be commented 
#when launching in the function 
#input.mp4 or input2.mp4 
print(main({'file': 'input.mp4', 'output': 'output_video.mp4'}))

import datetime                                                  
from random import sample  
from os import path
from time import time                                                           
import os

from jinja2 import Template

import boto3 

#SCRIPT_DIR = path.abspath(path.join(path.dirname(__file__)))

def main(args):

    # start timing
    start = datetime.datetime.now()
    name = args.get('username','djobiii2078')
    size = args.get('random_len',10000)
    cur_time = datetime.datetime.now()
    random_numbers = sample(range(0, 1000000), size)

    #download template file from AWS S3

    obj = boto3.client("s3",
                       aws_access_key_id="AWSKEYID",
                       aws_secret_access_key="AWSSECRET"
                       )
    download_begin = datetime.datetime.now() 

    obj.download_file(
            Filename = "template.html",
            Bucket = "swiftruntimes",
            Key = "template.html"
            )

    download_end = datetime.datetime.now()

    transform_begin = datetime.datetime.now() 
    template = Template( open('template.html', 'r').read())
    html = template.render(username = name, cur_time = cur_time, random_numbers = random_numbers)

    transform_end = datetime.datetime.now() 

    # end timing
    # dump stats 
    return {'result': html,
            'start_time': datetime.datetime.timestamp(start),
            'download_time': (download_end - download_begin)/datetime.timedelta(microseconds=1),
            'transform_time': (transform_end - transform_begin)/datetime.timedelta(microseconds=1), 
            'total_time': (transform_end - start)/datetime.timedelta(microseconds=1)
            }

# should be commented 
# if not used for debugging 

print(main({'username': 'djobiii2078', 'random_len': 512}))

#import boto3
#import numpy
#import pandas
import time 
import sys
#import json 
start = time.time()
#print(sys.meta_path)
#socketObjSpec = sys.meta_path[3].find_spec('socket')

end = time.time()
print("Time taken: ", end-start)

print("All files loaded")
#print(socketObjSpec)


sys.meta_path[3].find_spec('torch')
start = time.time()

import torch
end = time.time() 

print("Time taken json ", end-start)

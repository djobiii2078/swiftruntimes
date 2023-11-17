import signal, os 
from timeit import default_timer as timer 

#Main utility for the swift runtime routines
#@expand: fetches a remote copy of the previously discarded library
#   and uses zerocopy to prevent useless copies and speed the expansion
#
#@shrink: discard all imported libraries that are not in a specific list 
#The shrink does not check if the discarded libraries are currently being used --- thus it is the caller that should ensure that


#The list of essential libraries that should not be discarded
#For serverless, it is basically the libraries necessary for the runtime
#to determine that it should trigger the user's function

#extracted from https://github.com/apache/openwhisk-runtime-python/blob/master/core/python311Action/requirements.txt 

psl = [
        "beautifulsoup4",
        "httplib2",
        "kafka_python",
        "lxml",
        "python-dateutil",
        "requests",
        "scrapy",
        "simplejson",
        "virtualenv",
        "twisted",
        "netifaces",
        "timeit", #for time measurements 
        "setuptools"
    ]

shrink_msg = "Shrink runtime\n";
expand_msg = "Expand runtime\n"; 

shrink_time = 0;
expand_time = 0; 

shrink_flag = 0; 
expand_flag = 0; 

fsl_list = []; 
start_timer = 0; 

def handler(signum, frame):

    signame = signal.Signals(signum).name
    
    if(signame == "SIGSTOP"):
        
        shrink_flag = 1;
        start_timer = timer()
        #shrink routine 
        #Get the list of all modules 
        modulenames = set(sys.modules) & set(globals())
        fsl_list = [sys.modules[name] for name in modulenames] 

        for lib in fsl_list:
            print(lib," ")

        shrink_time = timer() - start_timer()


    if(signame == "SIGCONT"):
        expand_flag = 1; 
        start_timer = timer(); 
        #expand routine 
        expand_time = timer() - start_timer()


signal.signal(signal.SIGINT, handler)
signal.signal(signal.SIGHUP, handler)

while True:
    #Perform processing 
    if(shrink_flag):
        print(shrink_msg)
        print("Shrink took : ", shrink_time)
        shrink_flag = 0

    if(expand_flag):
        print(expand_msg)
        print("Expand took : ", expand_time)
        expand_flag = 0

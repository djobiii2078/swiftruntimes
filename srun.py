import signal
import sys
from timeit import default_timer as timer 
import uuid
import gc
from PIL import Image 
#from urllib.parse import unquote_plus
#import subprocess
import shutil
#import datetime
#import io
import boto3
#import urllib3
#import torchvision 




#Main utility for the swift runtime routines
#@expand: fetches a remote copy of the previously discarded library
#   and uses zerocopy to prevent useless copies and speed the expansion
#
#@shrink: discard all imported libraries that are not in a specific list 
#The shrink does not check if the discarded libraries are currently being used --- thus it is the caller that should ensure that


#The list of essential libraries that should not be discarded
#For serverless, it is basically the libraries necessary for the runtime
#to determine that it should trigger the user's function



class erun_faas:

	#extracted from https://github.com/apache/openwhisk-runtime-python/blob/master/core/python311Action/requirements.txt 

	def __init__( self ):
		signal.signal(signal.SIGINT, lambda signal, frame:self.handler_expand()) #expand
		signal.signal(signal.SIGHUP, lambda signal, frame:self.handler_shrink()) #shrink
		
		self.psl = [
		"beautifulsoup4",
		"httplib2",
		"kafka_python",
		"lxml",
		"python-dateutil",
		"requests",
		"scrapy",
		#necessary for erun shrink / expand mechanism
		"signal",
		"os",
		"sys",
		################################
		"simplejson",
		"virtualenv",
		"twisted",
		"netifaces",
		"timeit", #for time measurements 
		"setuptools",
        #built-in python modules necessary for the runtime at initialization (Modules/config.c --- from CPython source code) 
        "atexit",
        "faulthandler",
        "posix",
        "_signal",
        "_tracemalloc",
        "_codecs",
        "_collections",
        "errno",
        "_io",
        "itertools",
        "_sre",
        "_sysconfig",
        "_thread",
        "time",
        "_typing",
        "_weakref",
        "_abc",
        "_functools",
        "_locale",
        "_operator",
        "_stat",
        "_symtable",
        "pwd",
        "marshal",
        "_imp",
        "_ast",
        "_tokenize",
        "sys",
        "builtins",
        "gc",
        "_warnings",
        "_string",
		######### system base libraries ############
		## should be changed to consider specific runtimes 
		"sys", "builtins", "_frozen_importlib", "_imp", "_thread", "_warnings", "_weakref", "_io", "marshal", "posix", "_frozen_importlib_external", "time", "zipimport", "_codecs", "codecs", "encodings.aliases", "encodings", "encodings.utf_8", "_signal", "_abc", "abc", "io", "__main__", "_stat", "stat", "_collections_abc", "genericpath", "posixpath", "_sitebuiltins", "types", "importlib._bootstrap", "importlib._bootstrap_external", "warnings", "importlib", "importlib._abc", "itertools", "keyword", "_operator", "operator", "reprlib", "_collections", "collections", "_functools", "functools", "contextlib", "importlib.util", "importlib.machinery", "mpl_toolkits", "paste", "_distutils_hack", "site", "enum", "signal", "gc", "timeit", "_sre", "re._constants", "re._parser", "re._casefix", "re._compiler", "copyreg", "re", "platform", "atexit", "collections.abc", "token", "tokenize", "linecache", "textwrap", "traceback", "_weakrefset", "weakref", "_string", "string", "threading", "logging", "math", "_struct", "struct", "fnmatch", "errno", "zlib", "_compression", "_bz2", "bz2", "_lzma", "lzma", "_bisect", "bisect", "_random", "_sha512", "random", "tempfile", "ntpath", "urllib", "ipaddress", "urllib.parse", "pathlib", "__future__", "xml", "xml.parsers", "pyexpat.errors", "pyexpat.model", "pyexpat", "xml.parsers.expat.model", "xml.parsers.expat.errors", "xml.parsers.expat", "defusedxml.common", "defusedxml", "xml.etree", "xml.etree.ElementPath", "copy", "_elementtree", "xml.etree.ElementTree", "defusedxml.ElementTree", "cffi.lock", "cffi.error", "cffi.model", "cffi.api", "cffi"
		
		
	    ] 
		
		self.shrink_msg = "Shrink runtime\n";
		self.expand_msg = "Expand runtime\n"; 
		self.run_msg = "Running function\n"; 

		self.shrink_time=0
		self.expand_time=0

		self.shrink_flag=0
		self.expand_flag=0
		
		self.run_func = 0

		self.fsl_list = []
		self.fsl_addresses = []
		 

	#signal handler for 
	#expand and shrinking
	
	#SIGHUP
	def handler_shrink(self):

		self.shrink_flag = 1
		start_timer = timer()
		#shrink routine 
		#Get the list of all modules 
		if(len(self.fsl_list)):
			print("FSL already removed\n")
		else:
			
			#del sys.modules["shutil"]
			#del sys.modules["uuid"]
			#print(dir())
			for lib in list(sys.modules.keys()):
				if(lib not in self.psl): 
					#it belong to the fsl
					print("deleting fsl ", lib, ", sys.modules = ", sys.modules[lib], "\n")
                                        #get the addresses of the variable names
                                        #that point to the librairies that would be removed 
                                        #will be useful for RDMA/zero-copy web 

			#		boto3 = ""
					self.fsl_addresses.append(hex(id(lib)))
					self.fsl_list.append(lib)
					
					#gc.mark(sys.modules[lib]) 
					del sys.modules[lib]
		#boto3 = ""
		gc.collect()
		self.shrink_time = timer() - start_timer


	def handler_expand(self):
	
		self.expand_flag = 1; 
		start_timer = timer(); 
		#expand routine 
		self.expand_time = timer() - start_timer()
		
	def runFunc(self):
		#run function and wait 
		self.run_func=1

	
	def main_loop(self):
		while True:
			#Perform processing 
			if(self.shrink_flag == 1):
				print(self.shrink_msg)
				print("Shrink took : ", self.shrink_time)
				self.shrink_flag = 0
				
			if(self.expand_flag == 1):
				print(self.expand_msg)
				print("Expand took : ", self.expand_time)
				self.expand_flag = 0
			if(self.run_func == 1):
				print(self.run_msg) 
	
	
func = erun_faas()
func.main_loop()



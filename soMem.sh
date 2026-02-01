#!/bin/bash

#Get the sum of kb used by the so files loaded for the application
#the only parameter is the pid of the process 

usage()
{
	echo "$0 <pid>"
	echo "Print the memory (in kilobytes) used by .so objects for the process with pid <pid>"
}
echo ".so libs: "
sudo pmap -x $1 | grep so | awk '{sum+=$3;}END{print sum;}' 
echo ""

echo "Anon: "
sudo pmap -x $1 | grep anon | awk '{sum+=$3;}END{print sum;}'

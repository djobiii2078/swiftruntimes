#!/bin/bash 


#Check if openwhisk is installed 
#if it is not installed, let's install that 

#check if java 1.8 or 11 or < 17 is present on the server 
#Need Go installed
# install wsk openwhisk tool if not present 
git clone https://github.com/apache/openwhisk-cli
go build -o wsk 

echo 'export PATH=$PATH:$(pwd)/wsk' >> ~/.bashrc 

cd .. 

# install openwhisk playground
git clone https://github.com/apache/openwhisk.git
cd openwhisk
./gradlew core:standalone:bootRun

# configure wsk tool with correct parameters 

wsk property set \
  --apihost 'http://localhost:3233' \
  --auth '23bc46b1-71f6-4ed5-8c54-816aa4f8c502:123zO3xZCLrMN6v2BKK1dXYFpXlPkccOFqm12CdAsMgRU4VrNZ9lyGVCGuMDGIwP'

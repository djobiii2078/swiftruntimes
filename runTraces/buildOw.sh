#!/bin/bash 


#Check if openwhisk is installed 
#if it is not installed, let's install that 

#check if java 1.8 or 11 or < 17 is present on the server 
#Need Go installed
sudo apt install openjdk-11-jre-headless
sudo apt install golang-go go-bindata
sudo apt install nodejs npm
# install wsk openwhisk tool if not present 
git clone https://github.com/apache/openwhisk-cli
cd openwhisk-cli 
go get -u github.com/jteeuwen/go-bindata/...
go-bindata -pkg wski18n -o wski18n/i18n_resources.go wski18n/resources
go build 
go build -o wsk 

echo "export PATH=$PATH:$(pwd)/wsk" >> ~/.bashrc 

cd .. 

# install openwhisk playground
git clone https://github.com/apache/openwhisk.git
cd openwhisk
./gradlew core:standalone:bootRun

# configure wsk tool with correct parameters 

wsk property set \
  --apihost 'http://localhost:3233' \
  --auth '23bc46b1-71f6-4ed5-8c54-816aa4f8c502:123zO3xZCLrMN6v2BKK1dXYFpXlPkccOFqm12CdAsMgRU4VrNZ9lyGVCGuMDGIwP'

#!/bin/bash 

while true; do 
docker stats --no-stream >> $1 
sleep $2 
done 

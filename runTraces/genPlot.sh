#!/bin/bash 
#generate the plot for a a given function id 

imageid=$1
memmax=$2
basemem=$3
input=$4

if [ "$#" -ne 3 ]; then 
	echo "Incorrect number of arguments"
	echo "Usage"
	echo "$0 <imgid> <memmax> <basemem> <input>"
	echo " where:"
	echo "		<imgid> the image of the docker instance to analyze"
	echo "		<memmax> the maximum memory configured for the instance"
       	echo "		<basemem> the memory used by the container with no running application"	
echo "		<input> the input file to use for analysis"
fi 

#the goal is to create a file which can be ingested
#by the gnuplot script file 
#we want a file in the format timestamp	memmax	mem basemem	

echo "Parsing $input file and extracting plot data"

grep "$imageid" $input | awk -F' {2,}' '{print $3" "$4}' | awk -F"/" '{print $1}' | awk -F'MiB' '{print $1}' | awk -F'%' '{print NR" " "max" $2 " base " $1/2}' > plot_data_$imageid

echo "Fitting maxmem and basemem in plot data"

sed -i "s/max/$maxmem/g" plot_data_$imageid
sed -i "s/base/$basemem/g" plot_data_$imageid 

cd plots
cp plot_X.gnu plot_$imageid.gnu
sed -i "s/INPUT.txt/plot_data_$imageid/g" plot_$imageid.gnu 
sed -i "s/FILENAME.pdf/plot_$imageid.pdf/g" plot_$imageid.gnu

echo "Plot file plot_$imageid.gnu generated. Running gnuplot ..."

gnuplot plot_$imageid.gnu 

echo "Checkout plot_$imageid.pdf" 

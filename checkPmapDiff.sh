#!/bin/bash 

#reports the libraries that are not present in the 
#first file but are present in the second 

usage()
{
	echo "$0 <pmap_file_1> <pmap_file_2>"
	echo "Reports the librarieis that are present in <pmap_file_1> and are not present in <pmap_file_2>"
	echo "<pmap_file_1> and <pmap_file_2> are the files containing the different diffs"
}

reportdiff()
{
	echo "" > allreadyprocessed	
	for lib in $(cat $1 | awk  '{print $4}'); do 
		present=$(grep -F "$lib" $2 | wc -l)
		if [ $present -lt 1 ]; then
			if [ $(grep -F "$lib" allreadyprocessed | wc -l) -lt 1 ]; then
				echo $lib
				echo $lib >> allreadyprocessed
			fi 
		fi
	done
}

reportdiff $1 $2 

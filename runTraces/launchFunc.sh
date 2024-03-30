#!/bin/bash 
# Run a function by following traces from Cloud providers 
# You should specify the function, type of traces to use, and an id to use mimic the function

#./launcherFunc.sh <func> <idtrace> <provider> <logPeriod>
func=$1
idtrace=$2
provider=$3
logperiod=$4
RANDOMSEED=$RANDOM

alibaba_traces="/home/bmvondod/Downloads/ATC21_FaaSNet_ColdStart_Dataset_AlibabaCloud_FunctionCompute"
azure_traces="/home/bmvondod/Downloads/"
huawei_traces="" # not available 
meta_traces="" # not available
aws_traces="" # not available


#check number of parameters 

if [ "$#" -ne 4 ]; then
	echo "Incorrect number of arguments"
	echo "Usage"
	echo "$0 <func> <idtrace> <provider> <logPeriod>"
	echo "	where:"
	echo "		<func> the function name --- must be registered in openwhisk"
	echo "		<idtrace> the id of the function to use in the trace --- must exist in the provider's trace used"
	echo "		<provider> the name of the provider for the trace to be leveraged:"
	echo "			ex: Alibaba_01, Alibaba_02, Azure"
	echo "		<logPeriod> the periodic log interval to collect stats from docker"
	exit 
fi


#Get the epoch file into a tmp file 
#tmp_epoch_faas
 
if [ "$provider" == "Alibaba_01" ]; then 
	grep $idtrace $alibaba_traces/region_01.csv | awk -F',' '{print $2}' > /tmp/tmp_epoch_faas_$RANDOMSEED	

elif [ "$provider" == "Alibaba_02" ]; then 
	grep $idtrace $alibaba_traces/region_02.csv | awk -F',' '{print $2}' > /tmp/tmp_epoch_faas_$RANDOMSEED
elif [ "$provider" == "Azure" ]; then 
	grep $idtrace $azure_traces/AzureFunctionsInvocationTraceForTwoWeeksJan2021.txt | awk -F',' '{print $3}' > /tmp/tmp_epoch_faas_$RANDOMSEED 
elif [ "$provider" == "Huawei" ]; then 
	echo "not yet implemented"
	exit
elif [ "$provider" == "Amazon" ]; then 
	echo "not yet implemented"
	exit
elif [ "$provider" == "Meta" ]; then 
	echo "not yet implemented"
	exit
else 
	echo "No viable case chosed"
	exit	##
fi

#trigger file read and log trace collect 
#assume Openwhisk is up running 
# results will be appended in run_$RANDOMSEED/res.txt
startTimestamp=$(head -n 1 /tmp/tmp_epoch_faas_$RANDOMSEED)
mkdir run_$RANDOMSEED
./logDockerStats.sh run_$RANDOMSEED/res.txt $logperiod & 
logPID=$!


#Start firing functions 
sleepValue=0

while read -r line; do
	echo "line = $line, startTimestamp=$startTimestamp"
	let sleepValue=$line-$startTimestamp
	wsk action invoke $func 
	echo "Lanched $func. Sleeping for $sleepValue"
	startTimestamp=$line
	sleep $sleepValue
done < /tmp/tmp_epoch_faas_$RANDOMSEED

kill -9 $logPID
echo "Successfully launched the simulation"
echo "Checkout the logs in run_$RANDOMSEED/res.txt" 




#!/bin/bash

max=1000000
for (( i=0; i <= $max; ++i ))
do
	var=$(( RANDOM % $max ))
	echo $var
	#curl http://172.22.216.125:8689/populabanco
	curl http://172.22.216.125:8689/
	curl http://172.22.216.125:5000/
	#curl http://172.26.231.208:5000/
done

#!/bin/bash

process_num=$1
event_rate=$2
load_duration_sec=$3

for (( i=0; i<$process_num; i++))
do
    echo "Starting a new test load process #$i"
    python test-load/test-load.py $event_rate $load_duration_sec &
done

#!/bin/bash
CONCURRENT_COUNT=10
NUM_PROCESS=0

PATTERN=596
for i in `seq 333 596`; do
    (( NUM_PROCESS++ ))
    python3 test_parallel.py $i &

    if `test $NUM_PROCESS -ge $CONCURRENT_COUNT `; then 
        wait
        NUM_PROCESS=0;
    fi
    
done;

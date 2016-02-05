#!/bin/bash
CONCURRENT_COUNT=10
NUM_PROCESS=0

PATTERN=596
DIRECTORY=_
for i in `seq 333 596`; do
    (( NUM_PROCESS++ ))
    mkdir $DIRECTORY$NUM_PROCESS
    cp test_parallel.py $DIRECTORY$NUM_PROCESS
    cp -r lib $DIRECTORY$NUM_PROCESS
    cd $DIRECTORY$NUM_PROCESS

    python3 test_parallel.py $i &

    cd ..

    if `test $NUM_PROCESS -ge $CONCURRENT_COUNT `; then 
        wait
        NUM_PROCESS=0;
    fi
    
done;

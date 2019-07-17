#!/bin/bash

work="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

results_dir=$work/results
logs_dir=$work/logs
bin_dir=$work/bin

mkdir logs_dir &> /dev/null
mkdir results_dir &> /dev/null

tag="thesis"
gc="zgc"
max_heap="4g"
young_heap="4g"

# Number of objects where each object occupies 1MB
size=1000

# Percentage of Reads = Reads
# Percentage of Writes = 100 - Reads
reads=50

# Replace the desired gc
#gc="zgc"
gc="g1"
#gc="cms"
#gc="shenandoah"
#gc="zing"

function run {
    gc_script=$1

    sufix=$tag-$gc-$max_heap-$young_heap-`date +%s`
    echo "Starting $sufix"

    echo $gc_script
    $gc_script -jar "Thesis.jar" $size $reads &> $logs_dir/thesis.log

    # Backup Logs "$GC-$max_heap-$min-heap-gc.log"
    echo -n "Saving logs to $results_dir/$sufix ..."
    mkdir -p $results_dir/$sufix
    cp $work/logs/thesis.log $results_dir/$sufix/
    cp /tmp/jvm.log $results_dir/$sufix
    echo "done!"
    echo "Finished $sufix"
}

run $bin_dir/$gc-java

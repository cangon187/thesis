#!/bin/bash

work="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

results_dir=$work/results
graphs_dir=$work/graphs
logs_dir=$work/logs
bin_dir=$work/bin

mkdir $logs_dir &> /dev/null
mkdir $results_dir &> /dev/null
mkdir $graphs_dir &> /dev/null

tag="test"
max_heap="4g"
young_heap="1g"

size=2M

function runSet {
    day=`date +"%d:%m:%y"`
    time=`date +"%H:%M:%S"`
    reads=$1
    oper=$2
    run $bin_dir/cms-java cms
    run $bin_dir/g1-java g1
    run $bin_dir/shenandoah-java shenandoah
    run $bin_dir/zgc-java zgc
}

function run {
    gc_script=$1
    gc=$2

    prefix=$tag-$max_heap-$young_heap-$size-$reads-$oper-$day-$time
    sufix=$gc
    echo "Starting $sufix"

    $gc_script -jar "Microbench.jar" $size $reads $oper &> $logs_dir/microbench.log

    # Backup Logs "$GC-$max_heap-$min-heap-gc.log"
    echo "Saving logs to $results_dir/$prefix/$sufix ..."
    mkdir -p $results_dir/$prefix/$sufix
    cp $logs_dir/microbench.log $results_dir/$prefix/$sufix
    cp /tmp/jvm.log $results_dir/$prefix/$sufix
    echo "Finished $prefix/$sufix"
    echo
}

for OPS in 100M
do
    for PERCENT in 10
    do
        runSet $PERCENT $OPS
    done
done





build=~/bin/thesis-coliveira
results_dir=~/results/thesis-coliveira
logs_dir=~/logs
working_dir=/tmp/thesis-coliveira

tag="thesis"
gc="zgc"
max_heap="4g"
young_heap="4g"

rm -rf $working_dir &> /dev/null
mkdir $working_dir &> /dev/null

sufix=$tag-$gc-$max_heap-$young_heap-`date +%s`
echo "Starting $sufix"

# Number of objects where each object occupies 1MB
size=1000

# Percentage of Reads = Reads
# Percentage of Writes = 100 - Reads 
reads=50

# Replace the desired gc
#~/bin/g1-java
#~/bin/zing-java
#~/bin/zgc-java
#~/bin/shenandoah-java
#~/bin/cms-java
~/bin/zgc-java -jar "Thesis.jar" $size $reads &> $logs_dir/thesis.log

# Backup Logs "$GC-$max_heap-$min-heap-gc.log"
echo -n "Saving logs to $results_dir/$sufix ..."
mkdir -p $results_dir/$sufix
cp ~/logs/thesis.log $results_dir/$sufix/
cp /tmp/jvm.log $results_dir/$sufix
echo "done!"
echo "Finished $sufix"

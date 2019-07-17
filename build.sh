#!/bin/bash

work="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

# Compile the java file
javac -d $work/build $(find $work/src -name "*.java")

# Build the Jar File
jar -cfe $work/Thesis.jar ist.utl.pt.microbenchmark.Microbench -C $work/build .

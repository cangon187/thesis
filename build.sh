# Compile the java file
javac -d . ./src/ist/utl/pt/microbenchmark/*.java

# Build the Jar File
jar -cvfm Microbench.jar MANIFEST.MF ist/utl/pt/microbenchmark/*.class


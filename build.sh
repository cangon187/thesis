# Compile the java file
rm -r ./ist/
javac -d . ./src/ist/utl/pt/microbenchmark/Microbench.java

# Build the Jar File
jar -cvfm Microbench.jar MANIFEST.MF ist/utl/pt/microbenchmark/*.class 
# Compile the java file
javac -d . *.java

# Build the Jar File
jar -cvfm Thesis.jar MANIFEST.MF thesis/*.class


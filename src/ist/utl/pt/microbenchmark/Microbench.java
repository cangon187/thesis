package ist.utl.pt.microbenchmark;

import java.util.HashMap;
import java.util.Random;

public class Microbench {

    // Object size in KB
    static int objectSize = 1;

    // Create HashMap
    HashMap<String, GenericObject> population;

    public Microbench(int datasize) {

        population = new HashMap<>();

        for (int i = 0; i < datasize; i++) {
            population.put(String.valueOf(i), new GenericObject());
        }
    }

    static class GenericObject {

        public long[] obj;

        public GenericObject() {
            // long size 8 * 128 = 1024 bytes = 1KB * ObjectSize 
            obj = new long[128 * objectSize];
        }

        public void writeObject(long[] newObj) {
            this.obj = newObj;
        }
    }
    
    public static double randomNumber() {
        return 0.0f + (1.0f - 0.0f) * new Random().nextDouble();
    }
    
    public static void main(String[] arg) {
        if (arg.length == 3) {
            try
            {
                int dataSize = Integer.parseInt(arg[0]);
                int nOperations = Integer.parseInt(arg[2]);
                double readPercentage = Integer.parseInt(arg[1]) / 100;
                Random rand = new Random();
                Microbench dataSet = new Microbench(dataSize);

                for(int i=0; i<nOperations; i++) {
                    if (randomNumber() < readPercentage){
                        GenericObject object = dataSet.population.
                                get(String.valueOf(rand.nextInt(dataSize-1)));
                        System.out.println(object);
                    } 
                    else {
                        dataSet.population.
                                get(String.valueOf(rand.nextInt(dataSize-1))).
                                writeObject(new long[128 * objectSize]);
                    }
                }  
            }
            catch(Exception e)
            {
                System.out.println(e);
            }
        }
        else
        {
            System.out.println("Input is not valid");
        }
    }
}
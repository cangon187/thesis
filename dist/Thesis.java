package thesis;

import java.util.HashMap;
import java.util.Random;

public class Thesis {

    // Object size in KB
    static int objectSize = 1;

    // Create HashMap
    HashMap<String, GenericObject> population;

    public Thesis(int datasize) {

        population = new HashMap<>();

        for (int i = 0; i < datasize; i++) {
            population.put(String.valueOf(i), new GenericObject());
        }
    }

    protected HashMap<String, GenericObject> getPopulation() {
        return this.population;
    }

    static class GenericObject {

        private long[] obj;

        public GenericObject() {
            // long size 8 * 128 = 1024 bytes = 1KB * ObjectSize 1KB = 1MB
            obj = new long[128 * objectSize];
        }

        public long[] getObject() {
            return this.obj;
        }

        public void writeObject(long[] newObj) {
            this.obj = newObj;
        }
    }

    public static double randomNumber() {
        return 0.0f + (1.0f - 0.0f) * new Random().nextDouble();
    }
    
    public static void main(String[] arg) {
        if (arg.length == 2) {
            try
            {
                int dataSize = Integer.parseInt(arg[0]);
                Thesis dataSet = new Thesis(dataSize);
                while (true) {
                    dataSet.getPopulation().keySet().forEach((String str) -> {
                        if (randomNumber() < (double) Integer.parseInt(arg[1]) / 100) {
                            long[] object = dataSet.getPopulation().get(str).getObject();
                        } 
                        else {
                            dataSet.getPopulation().get(str).
                                    writeObject(new long[128 * objectSize]);
                        }
                    });
                }
            }
            catch(Exception e )
            {
                System.out.println(e);
            }
        }
        else
        {
            System.out.println("Input : java -jar Thesis.jar SIZE_MB READ_PERCENT");
        }
    }
}

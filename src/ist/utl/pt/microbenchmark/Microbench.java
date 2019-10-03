package ist.utl.pt.microbenchmark;

import java.nio.ByteBuffer;
import java.util.HashMap;
import java.util.Random;
import java.util.Timer;
import java.util.TimerTask;

public class Microbench{
        
    // Object size in KB
    static int objectSize = 1;

    // Declare data struct to hold objects
    HashMap<String, GenericObject> population;

    public Microbench(int datasize) {
        
        // Initialize data struct
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
    
    // Used to count and print the throughput
    static class RemindTask extends TimerTask {
        public int counter = 0;
        public int timer = 0;
        
        @Override
        public void run() {
          timer += 100;
          System.out.println("[" + timer + "ms] Throughput: " + counter);
          counter = 0;
        }
    }

    @SuppressWarnings("UseSpecificCatch")
    public static void main(String[] arg) {
        if (arg.length == 3) {
            try
            {
                int tmp = 0;
                int dataSize = Integer.parseInt(arg[0].substring(0, arg[0].length()-1))*1000000;
                int nOperations = Integer.parseInt(arg[2].substring(0, arg[2].length()-1))*1000000;
                double readPercentage = (double) Integer.parseInt(arg[1]) / 100;
                
                Random rand = new Random();
                ByteBuffer buffer = ByteBuffer.allocateDirect(nOperations*8);
                for(int i=0; i<nOperations; i++){
                    buffer.putDouble(rand.nextDouble());
                }
                buffer.flip();

                Microbench dataSet = new Microbench(dataSize);
                
                // Used to print the throughput every 100ms
                RemindTask rmdtask = new RemindTask();
                Timer timer = new Timer(true);
                timer.schedule(rmdtask, 0, 100);
                
                for(int i=0; i<nOperations; i++) {
                    if (buffer.getDouble() < readPercentage){
                        GenericObject object = dataSet.population.
                                get(String.valueOf(rand.nextInt(dataSize-1)));
                        tmp += object.obj[0];
                    } 
                    else {
                        dataSet.population.
                                get(String.valueOf(rand.nextInt(dataSize-1))).
                                writeObject(new long[128 * objectSize]);
                    }
                    // Increment throughput counter
                    rmdtask.counter++;
                }
                timer.cancel();
                timer.purge();
                double mean = ((nOperations / rmdtask.timer) * 100) + tmp;
                System.out.println("[Mean] Throughput: " + mean);
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
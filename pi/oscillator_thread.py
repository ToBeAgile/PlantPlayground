import time
from time import sleep
import threading
import math, itertools

DAC1_FREQUENCY = 1
DAC1_SAMPLE_RATE = 512
DAC1_INTERVAL = 1
DAC2_FREQUENCY = 1
DAC2_SAMPLE_RATE = 512
DAC2_INTERVAL = 1

class oscillator():
    def __init__(self, frequncy, sample_rate, interval):
        self.frequency = frequncy
        self.sample_rate = sample_rate
        self.interval = self.frequency * self.sample_rate
        
    def get_sine_oscillator(self):
        increment = (2 * math.pi * self.frequency)/ self.sample_rate
        return (math.sin(v) for v in itertools.count(start=0, step=increment))
    
def launch_thread1(freq, rate, interval):
        osc = oscillator(freq, rate, interval)
        gen = osc.get_sine_oscillator()
        
        while True:
            print("Thread 1: " + str(next(gen)))
            sleep(interval)
        
def launch_thread2(freq, rate, interval):
        osc = oscillator(freq, rate, interval)
        gen = osc.get_sine_oscillator()
        
        while True:
            print("Thread 2: " + str(next(gen)))
            sleep(interval)
 
def main():
    #create and start thread
    t1 = threading.Thread(target=launch_thread1, args=(DAC1_FREQUENCY, DAC1_SAMPLE_RATE, DAC1_INTERVAL))
    t2 = threading.Thread(target=launch_thread2, args=(DAC2_FREQUENCY, DAC2_SAMPLE_RATE, DAC2_INTERVAL))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    #sleep(10)
    #t.stop()
    exit()

if __name__ == "__main__":
    main()
import Adafruit_ADS1x15
import time
import sys
import timeit
#from pythonosc.udp_client import SimpleUDPClient

sys.path.insert(1, '/home/pi/Documents/Code/PlantPlayground')
from pi.ADS1115Reader import *

"""
class ChannelInfo:
    channel_number
    channel_status = 'closed'
    channel_gain
    channel_data_rate
    channel_sleep
    channel_volts_per_division
    
"""    
    
class ADCStreamReader:
    
    GAIN = 16
    DATA_RATE = 8 # 8, 16, 32, 64, 128, 250, 475, 860

    SLEEP = 2
    NUMBEROFCHANNELS = 2
    DIFFERENTIAL1 = 0 
    DIFFERENTIAL2 = 3

    CHANNEL0 = 0
    CHANNEL1 = 1
    CH0SLEEPTIME = 1
    CH1SLEEPTIME = 1

    adc = Adafruit_ADS1x15.ADS1115()
    volts_per_division_table = {0:6.144, 1:4.096, 2:2.048, 4:1.024, 8:0.512, 16:0.256}
    voltsPerDivision = 0
    status = 'close'
    gain = 16
    data_rate = 8
    sleep = 1
    channel = 0
    differential = 0
    
    ip = "127.0.0.1"
    port = 1337

    #client = SimpleUDPClient(ip, port)  # Create client

    
    def __init__(self):
       #self.channel = channel
        dummy = 0

    # Store channels separately on object 
    def open(self, differential, gain, data_rate, sleep):
        self.differential = differential
        self.gain = gain
        self.data_rate = data_rate
        self.sleep = sleep
        #self.voltsPerDivision = ((2 * self.volts_per_division_table[self.gain])/65535)*1000
        return self.differential
    
    def read(self, differential):
        time.sleep(self.sleep)
        self.differential_value = self.adc.read_adc_difference(self.differential, self.gain, self.data_rate)
        return self.differential_value
    
    def read_without_sleep(self, differential):
        #time.sleep(self.sleep)
        self.differential_value = self.adc.read_adc_difference(self.differential, self.gain, self.data_rate)
        return self.differential_value



    def broadcastOSC(self):
            self.d0 = self.open(differential=0, gain=16, data_rate=860, sleep=0)
            self.d3 = self.open(differential=3, gain=16, data_rate=860, sleep=0)

            try:
                for x in range(1, 100):
                    # for each channel read(self, channel, gain, data_rate, sleep):
                    c0_value = self.adc.read_adc_difference(self.d0, self.gain, self.data_rate)
                    self.client.send_message("/PP01/ADC0/RAW/", c0_value)   # Send float message

                    c3_value = self.adc.read_adc_difference(self.d3, self.gain, self.data_rate)
                    self.client.send_message("/PP01/ADC1/RAW/", c3_value)   # Send float message
                    """
                    now = datetime.datetime.now()
                    #print("Value = ", value)
                    print((now.strftime("%H:%M:%S:%f"), (round((c0_value), 4)), (round((c1_value), 4))))
                    dl.write(((now.strftime("%H:%M:%S:%f")), (round((c0_value), 4)), (round((c1_value), 4))))
                    #csvwriter.write_voltage(name="Diff_V_1: ", value=value)
                    """
            except KeyboardInterrupt:
                    GPIO.cleanup()
            
      


# channel 0 is the control (a potato) gets read a second every minute
#reader.open(channel=CHANNEL0, gain=GAIN, data_rate=DATA_RATE, sleep=CH0SLEEPTIME) #open channel 0 stream
#reader.open(channel=CHANNEL1, gain=GAIN, data_rate=DATA_RATE, sleep=CH1SLEEPTIME) #open channel 1 stream

#print(timeit.timeit(lambda: reader.read(DIFFERENTIAL1, GAIN, DATA_RATE, 0), number=1))





"""import os
import errno
import time
import random

class DataEndpoint:
    def __init__(self, pipe_path):
        self.pipe_path = pipe_path
        print("creating pipe {}".format(pipe_path))
        # os.mkfifo(self.pipe_path)
        

    def __del__(self):
        print("deleting pipe {}".format(self.pipe_path))
        

    def send_data(self, data):
        self.pipe = open(self.pipe_path, "w")
        self.pipe.write(data)
        self.pipe.close();

consumers = []
"""

# set up all of the pipes that will consume data
# for entry in os.scandir("/tmp/plants"):
#     # consumers.append(lambda data_val: expression)
#     consumers.append(DataEndpoint(entry.path))

# while True:
#     data = random.randrange(100)
#     print("Sending data: {}".format(data))
#     for consumer in consumers:
        
#         consumer.send_data(str(data))

#     time.sleep(5)
import Adafruit_ADS1x15
import time
import sys
import timeit
import cmd, logging, smbus, RPi.GPIO as GPIO

#from pythonosc.udp_client import SimpleUDPClient

sys.path.insert(1, '/home/pi/Documents/Code/PlantPlayground')
from pi.ADS1115Runner import *
 
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

    ads1115Runner = ADS1115Runner()
    adc = Adafruit_ADS1x15.ADS1115()
    volts_per_division_table = {0:6.144, 1:4.096, 2:2.048, 4:1.024, 8:0.512, 16:0.256}
    voltsPerDivision = 0
    status = 'close'
    gain = 16
    data_rate = 8
    sleep = 0
    channel = 0
    differential = 0
    value = 0
    value_raw = 0
    
    ip = "127.0.0.1"
    port = 1337

    #client = SimpleUDPClient(ip, port)  # Create client

    
    def __init__(self):
       #self.channel = channel
        pass

    # Store channels separately on object 
    def open(self, reader_type, channel, gain, data_rate, sleep):
        self.reader_type = reader_type
        self.channel = channel
        self.gain = gain
        self.data_rate = data_rate
        self.sleep = sleep
        self.voltsPerDivision = ((2 * self.volts_per_division_table[self.gain])/65535)*1000
        if (self.reader_type == 'differential_i2c'):
            #config_string = '1-000-111-1-000-0-0-0-11'
            config_string = '1-000-111-1-000-0-0-0-11'
            self.ads1115Runner.i2c_reader_init(config_string)
            #adc = ADCStreamReader()
            #resetChip()
            # compare with configuration settings from ADS115 datasheet
            # start single conversion - AIN2/GND - 4.096V - single shot - 8SPS - X
            # - X - X - disable comparator
            #conf = prepareLEconf('1-000-111-1-100-1-0-0-11')
            #conf = prepareLEconf('0-000-111-1-100-1-0-0-11')
        return self.channel
    
    def read(self, channel):
        if (self.reader_type == 'differential' ):
            time.sleep(self.sleep)
            self.differential_value = self.adc.read_adc_difference(self.channel, self.gain, self.data_rate)
            return self.differential_value #* self.voltsPerDivision
        elif (self.reader_type == 'single_ended'):
            time.sleep(self.sleep)            
            self.differential_value = self.adc.read_adc(self.channel, self.gain, self.data_rate)
            return self.differential_value #* self.voltsPerDivision
        elif (self.reader_type == 'differential_i2c'):
            self.value_raw = self.ads1115Runner.i2c_read(channel)
            return self.value_raw #* self.voltsPerDivision


    def read_without_sleep(self, differential):
        #time.sleep(self.sleep)
        self.differential_value = self.adc.read_adc_difference(channel, self.gain, self.data_rate)
        return self.differential_value * self.voltsPerDivision


    """     
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

                now = datetime.datetime.now()
                #print("Value = ", value)
                print((now.strftime("%H:%M:%S:%f"), (round((c0_value), 4)), (round((c1_value), 4))))
                dl.write(((now.strftime("%H:%M:%S:%f")), (round((c0_value), 4)), (round((c1_value), 4))))
                #csvwriter.write_voltage(name="Diff_V_1: ", value=value)

        except KeyboardInterrupt:
            GPIO.cleanup()
            
    """      


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
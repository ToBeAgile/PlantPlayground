import Adafruit_ADS1x15
import unittest
import time
        

class ADS1115Reader:
    
    adc = Adafruit_ADS1x15.ADS1115()
    stream_info_dict = {0:6.144, 1:4.096, 2:2.048, 4:1.024, 8:0.512, 16:0.256}
    status = 'close'
    gain = 0
    data_rate = 0
    sleep = 1
    channel = 0
    
    def __init__(self):
       #self.channel = channel
        dummy = 0
        
        
    def open(self, channel, gain, data_rate, sleep):
        self.channel = channel
        self.gain = gain
        self.data_rate = data_rate
        self.sleep = sleep
        self.voltsPerDivision = ((2 * self.stream_info_dict[self.gain])/65535)*1000
    
    def read(self):
        dummy = self.adc.read_adc_difference(self.channel, self.gain, self.data_rate)
        time.sleep(self.sleep)
        value = self.adc.read_adc_difference(self.channel, self.gain, self.data_rate)
        value *= self.voltsPerDivision
        return value
    


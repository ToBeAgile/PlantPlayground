import Adafruit_ADS1x15
import unittest
import StreamInfo
import time
        

class ADS1115Reader:
    
    adc = Adafruit_ADS1x15.ADS1115()
    stream_info = []
    
    def __init__(self):
       #self.channel = channel
        dummy = 0
        
    def open(self, channel, gain, data_rate, sleep):
        si = StreamInfo.StreamInfo('open', gain, data_rate, sleep)
        self.stream_info.append(si)
         
    def is_channel_open(self, channel):
        #return channelCollection;
        si = self.stream_info[channel]
        return si.status
    
    def get_gain(self, channel):
        return self.stream_info[channel].gain
    
    def get_data_rate(self, channel):
        return self.stream_info[channel].data_rate
    
    def get_sleep(self, channel):
        return self.stream_info[channel].sleep
    
    def read(self, channel):
        dummy = self.adc.read_adc_difference(channel, self.get_gain(channel), self.get_data_rate(channel)) # Throw out first value
        time.sleep(self.get_sleep(channel))
        value = self.adc.read_adc_difference(channel, self.get_gain(channel), self.get_data_rate(channel))
        return value
    


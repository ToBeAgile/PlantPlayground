import Adafruit_ADS1x15
import time

"""
class ChannelInfo:
    channel_number
    channel_status = 'closed'
    channel_gain
    channel_data_rate
    channel_sleep
    channel_volts_per_division
    
"""    

class ADS1115Reader:
    
    adc = Adafruit_ADS1x15.ADS1115()
    volts_per_division_table = {0:6.144, 1:4.096, 2:2.048, 4:1.024, 8:0.512, 16:0.256}
    voltsPerDivision = 0
    status = 'close'
    gain = 16
    data_rate = 8
    sleep = 1
    channel = 0
    
    def __init__(self):
       #self.channel = channel
        dummy = 0
        
    def open(self, differential, gain, data_rate, sleep:float) -> None:
        self.differential = differential
        self.gain = gain
        self.data_rate = data_rate
        self.sleep = sleep
        self.voltsPerDivision = ((2 * self.volts_per_division_table[self.gain])/65535)*1000
    
    def read(self, differential, gain, data_rate, sleep):
        # dummy = self.adc.read_adc_difference(self.channel, self.gain, self.data_rate)
        if (sleep >= 0):
            time.sleep(sleep)
        value = self.adc.read_adc_difference(differential, gain, data_rate)
        return value * self.voltsPerDivision
    


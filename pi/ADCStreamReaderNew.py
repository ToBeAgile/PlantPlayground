from __future__ import print_function
from time import sleep
from sys import stdout
from daqhats import mcc128, OptionFlags, HatIDs, HatError, AnalogInputMode, \
    AnalogInputRange
from daqhats_utils import select_hat_device, enum_mask_to_string, \
    input_mode_to_string, input_range_to_string

import Adafruit_ADS1x15
import time
import sys
import timeit
import cmd, logging, smbus2, RPi.GPIO as GPIO

sys.path.insert(1, '/home/pi/grove.py/')
from grove.adc import ADC

#from pythonosc.udp_client import SimpleUDPClient

sys.path.insert(1, '/home/pi/Documents/Code/PlantPlayground')
from pi.ADS1115Runner import *

from abc import ABC, abstractmethod

'''
DAQStreams.py Todo:
    1. Figure out how to do differential reads and create a stream type for it
    1. Refactor open and read to strategies, extracting rules to an abstract factory that returns both objects
'''
# ADCStreamInfo contains everything needed to configure, open, read, and close an ADCStream

class ADCStreamInfo:
    #General settings
    sensor_type = 'mcc_single_value_read'
    sleep_between_reads = -1 # -1 = don't give away the time slice
    number_of_channels = 4
    channels = (True, True, True, True)
    #MCC128-specific settings
    analog_input_range = AnalogInputRange.BIP_10V
    reader_type = 'differential' # or 'single-ended'

    #other DAQ
    gain = 16
    data_rate = 8
    
    def __init()__
        pass
    
class ADCStreamReaderFactory:
    def __init__(self):
        pass
        
    def getADCStream(self, ADCStreamInfo)
        self.ADCStreamInfo = ADCStreamInfo()
        
        return ADCStream
    

class ADCStream(ABC):
    def __init__(self, value):
        self.value = value
        super().__init__()
        
    @abstractmethod
    def openADC(self, adcStreamInfo):
        pass
    
    @abstractmethod
    def read(self):
        pass
    
class MCC128Daq(ADCStream):
    def __init__(self, value):
        self.value = value
        super().__init__()
        
    @abstractmethod
    def openADC(self, adcStreamInfo):
        pass
    
    @abstractmethod
    def read(self):
        pass



"""

class ChannelInfo:
    channel_number
    channel_status = 'closed'
    channel_gain
    channel_data_rate
    channel_sleep
    channel_volts_per_division
    
"""
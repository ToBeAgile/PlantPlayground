#TODO: create ADCStreamReader open and read strategies for all DAQ types
#TODO: Read all 4 channels, time and GUID in read()
#DONE:
# #
from __future__ import print_function
from daqhats import mcc128, OptionFlags, HatIDs, HatError, AnalogInputMode, \
    AnalogInputRange
from daqhats_utils import select_hat_device, enum_mask_to_string, \
    input_mode_to_string, input_range_to_string

from time import sleep
import sys
import datetime
import timeit, cmd, logging, smbus2, RPi.GPIO as GPIO
import Adafruit_ADS1x15
from abc import ABC, abstractmethod
import uuid

sys.path.insert(1, '/home/pi/grove.py/')
#from grove.adc import ADC

#from pythonosc.udp_client import SimpleUDPClient

sys.path.insert(1, '/home/pi/Documents/Code/PlantPlayground')
from pi.ADS1115Runner import *
#from pi.PPRemote import daqStreamSetting



class DaqStreamSettings:
    # General settings
    guid = uuid.uuid4()
    sleep_between_reads = -1  # -1 = don't give away the time slice
    sleep_between_channels = 0.25
    number_of_channels = 4
    low_chan = 0
    high_chan = 3
    channels = [True, True, True, True]
    sensor_type = 'mcc_single_value_read'
    reader_type_a = 'mcc_single_value_read'  # 'grove_gsr' # 'dummy_read' #'single_ended' #'differential_i2c' #'single_ended' #'differential'
    reader_type_b = 'mcc_single_value_read'  # 'grove_gsr' # 'dummy_read' #'single_ended' #'differential_i2c' #'single_ended' #'differential'

    # DaqStreamSettings are the most important settings for DaqStreamInfo

    # MCC128-specific settings
    analog_input_range = AnalogInputRange.BIP_10V
    reader_type = 'differential'  # or 'single-ended'
    options = OptionFlags.DEFAULT
    input_mode = AnalogInputMode.DIFF  # or SE
    input_range = AnalogInputRange.BIP_10V  # BIP_1V

    mcc_128_num_channels = mcc128.info().NUM_AI_CHANNELS[input_mode]
    sample_interval = 0.1  # 0.5  # Seconds


# DaqStreamInfo contains everything needed to configure, open, read, and close an DaqStream
class DaqStreamInfo:
    #General settings
    sleep_between_reads = DaqStreamSettings.sleep_between_reads
    sleep_between_channels = DaqStreamSettings.sleep_between_channels
    number_of_channels = DaqStreamSettings.number_of_channels
    low_chan = DaqStreamSettings.low_chan
    high_chan = DaqStreamSettings.high_chan
    channels = DaqStreamSettings.channels
    sensor_type = DaqStreamSettings.sensor_type
    
    #MCC128-specific settings
    analog_input_range = DaqStreamSettings.analog_input_range
    reader_type = DaqStreamSettings.reader_type
    options = DaqStreamSettings.options
    input_mode = DaqStreamSettings.input_mode
    input_range = DaqStreamSettings.input_range

    mcc_128_num_channels = DaqStreamSettings.mcc_128_num_channels
    sample_interval = DaqStreamSettings.sample_interval

    # ADS1115 specific
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
    
'''    
class ADCStreamReaderFactory:
    def __init__(self):
        pass
        
    def getADCStream(self, ADCStreamInfo):
        self.ADCStreamInfo = ADCStreamInfo()
        
        return DaqStream
'''    

class DaqStream(ABC):
    
    @abstractmethod
    def openDaq(self, DaqStreamInfo):
        pass
    
    @abstractmethod
    def readDaq(self):
        pass

    @abstractmethod
    def closeDaq(self, DaqStreamInfo):
        pass

def getGUID():
    id = uuid.uuid4()
    return id.hex


def getDateTime():
    return datetime.datetime.now()


class MCC128Daq(DaqStream):
    daqChannels = [0.0, 0.0, 0.0, 0.0]
    this_moment = datetime.datetime.now().strftime("%H:%M:%S:%f")

    def openDaq(self, DaqStreamInfo):
        self.DaqStreamInfo = DaqStreamInfo
        self.options = DaqStreamInfo.options
        self.low_chan = DaqStreamInfo.low_chan
        self.high_chan = DaqStreamInfo.high_chan
        self.input_mode = DaqStreamInfo.input_mode
        self.input_range = DaqStreamInfo.input_range

        self.mcc_128_num_channels = DaqStreamInfo.mcc_128_num_channels
        self.sample_interval = DaqStreamInfo.sample_interval
        self.guid = getGUID()
        #print(self.guid)

        try:
            # Ensure low_chan and high_chan are valid.
            if self.low_chan < 0 or self.low_chan >= self.mcc_128_num_channels:
                error_message = ('Error: Invalid low_chan selection - must be '
                                 '0 - {0:d}'.format(self.mcc_128_num_channels - 1))
                raise Exception(error_message)
            if self.high_chan < 0 or self.high_chan >= self.mcc_128_num_channels:
                error_message = ('Error: Invalid high_chan selection - must be '
                                 '0 - {0:d}'.format(self.mcc_128_num_channels - 1))
                raise Exception(error_message)
            if self.low_chan > self.high_chan:
                error_message = ('Error: Invalid channels - high_chan must be '
                                 'greater than or equal to low_chan')
                raise Exception(error_message)
            # Get an instance of the selected hat device object.
            address = select_hat_device(HatIDs.MCC_128)
            self.hat = mcc128(address)

            self.hat.a_in_mode_write(self.input_mode)
            self.hat.a_in_range_write(self.input_range)
            self.sensor = self.hat

        except (HatError, ValueError) as error:
            print('\n', error)
    
    @property
    def readDaq(self):
        self.this_moment = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S:%f")
        for ch in range(self.low_chan, self.high_chan + 1):
            if self.DaqStreamInfo.channels[ch] is True:
                self.daqChannels[ch] = self.hat.a_in_read(ch)
                if self.DaqStreamInfo.sleep_between_channels != -1:
                    sleep(DaqStreamInfo.sleep_between_channels)
        sensor_data = list()
        sensor_data = (self.guid, self.this_moment, self.daqChannels[0], self.daqChannels[1], self.daqChannels[2], self.daqChannels[2])
        #print(myDict + self.this_moment)
        #return_items = {'GUID:': daq.guid, 'Time: ': self.this_moment, 'Ch0: ': self.daqChannels[0], 'Ch1: ':self.daqChannels[1], 'Ch2: ':, self.daqChannels[2], 'Ch3: ': self.daqChannels[3]}
        print (sensor_data)
        return sensor_data #self.hat.a_in_read(0)

    @property
    def closeDaq(self):
        pass
'''    
        if self.DaqStreamInfo.channels[0] is True:
            ch0 = self.hat.a_in_read(0)
        if self.DaqStreamInfo.sleep_between_channels != -1:
            sleep(DaqStreamInfo.sleep_between_channels)
        if self.DaqStreamInfo.channels[1] is True:
            ch1 = self.hat.a_in_read(1)
        if self.DaqStreamInfo.sleep_between_channels != -1:
            sleep(DaqStreamInfo.sleep_between_channels)
        if self.DaqStreamInfo.channels[2] is True:
            ch2 = self.hat.a_in_read(2)
        if self.DaqStreamInfo.sleep_between_channels != -1:
            sleep(DaqStreamInfo.sleep_between_channels)
        if self.DaqStreamInfo.channels[3] is True:
            ch3 = self.hat.a_in_read(3)
        if self.DaqStreamInfo.sleep_between_channels != -1:
            sleep(DaqStreamInfo.sleep_between_channels)
'''
                #for channel in range(DaqStreamInfo.low_chan, DaqStreamInfo.high_chan):
            #if self.DaqStreamInfo.channels[channel] is True:
                #channel_readings[channel] = self.hat.a_in_read(channel)
            #if self.DaqStreamInfo.sleep_between_channels != -1:
                #sleep(DaqStreamInfo.sleep_between_channels)
        #@@@
        #for each chan in channels:
            #read(), wait()
        #return tuple (guid, now, channels[ch0, ch1, ch2, ch3])
            #print(self.guid, now, ch0, ch1, ch2, ch3)
'''
        #receive GUID, set date-time
        GUID = getGUID()
        date_time = getDateTime()
        ch[]
        #foreach channel, read channel, delay between channels
        for channel in range(0, 3):
            if DaqStreamInfo.channels[channel] == True:
                ch[channel] = self.hat.a_in_read(channel)
            else
                ch[channel] = None
            if DaqStreamInfo.sleep_between_reads >  -1:
                time.sleep(DaqStreamInfo.sleep_between_reads)
        return (GUID, date_time, ch[0], ch[1], ch[2], ch[3])
'''
# Constants
#CURSOR_BACK_2 = '\x1b[2D'
#ERASE_TO_END_OF_LINE = '\x1b[0K'


    

    
class GroveGSRSensor:
    def __init__(self, channel):
        self.channel = channel
        self.Daq = ADC()

    @property
    def GSR(self):
        value = self.adc.read(self.channel)
        return value
    
    
class ADCStreamReader:
    Grove = GroveGSRSensor    

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
    DaqInfo = DaqStreamInfo()
    daq = MCC128Daq()
    
    #ip = "127.0.0.1"
    #port = 1337
    #daq = MCC128Daq()
    #client = SimpleUDPClient(ip, port)  # Create client

    def __init__(self):
       #self.channel = channel
        pass

    # Store channels separately on object 
    def open(self, reader_type, channel, gain, data_rate, sleep):
        self.reader_type = reader_type
        self.channel = channel # change to tuple of 4 bools for each active channel
        self.gain = gain
        self.data_rate = data_rate
        self.sleep = sleep
        self.sensor = 0
        self.voltsPerDivision = ((2 * self.adcInfo.volts_per_division_table[self.gain])/65535)*1000
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
        elif (self.reader_type == 'grove_gsr'):
            self.sensor = GroveGSRSensor(int(0))

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
        elif (self.reader_type == 'dummy_read'):
            time.sleep(self.sleep)            
            return 99
        elif (self.reader_type == 'grove_gsr'):
            time.sleep(self.sleep)            
            return self.sensor.GSR

    def read_without_sleep(self, differential):
        #time.sleep(self.sleep)
        self.differential_value = self.adc.read_adc_difference(self.channel, self.gain, self.data_rate)
        return self.differential_value * self.voltsPerDivision

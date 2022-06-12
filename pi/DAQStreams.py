# DAQStreams.py 1.0 - May 8, 2022 (c)reated by David Scott Bernstein
# DAQStreams.py - Supports multiple DAQs, called by PPRemote.py
# Supported DAQs: MCC128, ADS1115, ADS1115i2c, ADS1256
#from __future__ import print_function
from time import sleep
import sys
import datetime
import timeit, cmd, logging
from abc import ABC, abstractmethod
import uuid

sys.path.insert(1, '/home/pi/Documents/Code/PlantPlayground/pi')
from DAQStreamInfo import *

def getGUID():
    id = uuid.uuid4()
    return id.hex

class DaqStream(ABC):
    daq_info = None
    channels = list()
    
    @staticmethod
    def getInstance():
        dsi = DAQStreamInfo()
        daq_info = dsi.getConfig(ini_file_name)
        #print('daqToUSE:' + daq_info.daq_to_use )
        if (daq_info.daq_to_use == 'MCC128Daq'):
            adc = MCC128Daq()
        elif (daq_info.daq_to_use == 'ADS1115Stream'):
            adc = ADS1115Stream()
        elif (daq_info.daq_to_use == 'ADS1115i2cStream'):
            adc = ADS1115i2cStream()
        elif (daq_info.daq_to_use == 'ADS1256Stream'):
            adc = ADS1256Stream()
        else:
            adc = ADS1115i2cStream()
        return adc

    def __init__(self):
        dsi = DAQStreamInfo()
        self.daq_info = dsi.getConfig(ini_file_name)
        self.channels = [0, 0, 0, 0]      
        self.number_of_channels = 0
        self.daqChannels = [0.0, 0.0, 0.0, 0.0]
        self.sleep_between_reads = 0
        self.sleep_between_channels = 0
        self.number_of_channels = 0
        self.channels = 0
        self.ads1256_sensor_type = 0
        self.low_chan = 0
        self.high_chan = 0
        self.guid = getGUID()
        self.this_moment = datetime.datetime.now().strftime("%H:%M:%S:%f")
        #set up for readDaq
        self.daq_method = None
        self.conversion_method = None
        
    #@abstractmethod
    def openDaq(self):
        # General settings        
        self.number_of_channels = self.daq_info.number_of_channels
        self.daqChannels = [0.0, 0.0, 0.0, 0.0]
        self.sleep_between_reads = int(self.daq_info.sleep_between_reads)
        # -1 = don't give away the time slice
        self.sleep_between_channels = float(self.daq_info.sleep_between_channels)
        self.number_of_channels = int(self.daq_info.number_of_channels)
        self.channels = self.daq_info.channels #[True, True, True, True] #self.daq_info.channels #[True, True, True, True] #self.daq_info.channels #
        #self.ads1115_sensor_type = 'differential_value_read' #'single_value_read' # 'differential_value_read'
        self.ads1256_sensor_type = self.daq_info.ads1256_sensor_type
        self.low_chan = int(self.daq_info.low_chan)
        self.high_chan = int(self.daq_info.high_chan)
        
        self.guid = getGUID()
        self.this_moment = datetime.datetime.now().strftime("%H:%M:%S:%f")
        #print("DaqStreams Open...")
        
    def readDaq(self):
        if self.daq_info.sleep_between_reads != -1:
            sleep(self.daq_info.sleep_between_reads)
        self.this_moment = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S:%f")
        for ch in range(self.daq_info.low_chan, self.daq_info.high_chan + 1):
            if self.daq_info.channels[ch] is True:
                #self.scan_mode == 0): # 0 = Single-ended input  8 channel; 1 = Differential input  4 channe 
                self.daqChannels[ch] =  self.daq_method(ch) * self.conversion_method() #self.ads1115Runner.i2c_read(ch) #self.adc.read_adc(ch, self.gain, self.data_rate)
                #self.ADC.ADS1256_GetChannalValue(ch) #self.ads1115Runner.i2c_read(ch) #self.adc.read_adc(ch, self.gain, self.data_rate)
                if self.daq_info.sleep_between_channels != -1:
                    sleep(self.daq_info.sleep_between_channels)
        sensor_data = list()
        sensor_data = (self.guid, self.this_moment, self.daqChannels[0], self.daqChannels[1], self.daqChannels[2], self.daqChannels[3])
        print ("DAQStream sensor data: " + str(sensor_data))
        return sensor_data

    def closeDaq(self):
        pass

class MCC128Daq(DaqStream):
    
    def openDaq(self):
        from daqhats import mcc128, OptionFlags, HatIDs, HatError, AnalogInputMode, \
            AnalogInputRange
        from daqhats_utils import select_hat_device, enum_mask_to_string, \
            input_mode_to_string, input_range_to_string

        dsi = DAQStreamInfo()
        daq_info = dsi.getConfig(ini_file_name)

        self.this_moment = datetime.datetime.now().strftime("%H:%M:%S:%f")
        self.guid = getGUID()
        self.daqChannels = [0.0, 0.0, 0.0, 0.0]
        
        #general config settings
        self.sleep_between_reads = daq_info.sleep_between_reads
        self.sleep_between_channels = daq_info.sleep_between_channels
        self.number_of_channels = daq_info.number_of_channels
        self.low_chan = daq_info.low_chan
        self.high_chan = daq_info.high_chan
        self.channels = daq_info.channels
        self.sensor_type = daq_info.sensor_type

        # MCC128-specific settings
        self.analog_input_range = daq_info.analog_input_range
        assert( self.analog_input_range == 'AnalogInputRange.BIP_10V')
        #self.reader_type = 'differential'  # or 'single-ended'
        self.reader_type = daq_info.reader_type
                
        self.options = daq_info.options
        self.input_mode = AnalogInputMode.DIFF
        #self.input_mode = daq_info.input_mode #AnalogInputMode.DIFF  # or SE
        if(daq_info.options == 'AnalogInputMode.DIFF'):
            self.input_mode = AnalogInputMode.DIFF
        elif(daq_info.options == AnalogInputMode.SE):
            self.input_mode = AnalogInputMode.SE
        #self.daq_info.input_range #AnalogInputRange.BIP_10V
        self.input_range = AnalogInputRange.BIP_10V 
        if (daq_info.input_range == AnalogInputRange.BIP_10V):    
            self.input_range = AnalogInputRange.BIP_10V  # BIP_1V
        elif (daq_info.input_range == AnalogInputRange.BIP_1V):
            self.input_range = AnalogInputRange.BIP_1V  # BIP_10V
        self.sample_interval = daq_info.sample_interval #0.1  # 0.5  # Seconds
        self.mcc_128_num_channels = daq_info.number_of_channels #mcc128.info().NUM_AI_CHANNELS[self.input_mode]
        self.myHatError = HatError

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

        except (self.myHatError, ValueError) as error:
            print('\n', error)
    
    def readDaq(self):
        if self.sleep_between_reads != -1:
            sleep(self.sleep_between_reads)
        self.this_moment = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S:%f")
        for ch in range(self.low_chan, self.high_chan + 1):
            if self.channels[ch] is True:
                self.daqChannels[ch] = self.hat.a_in_read(ch)
                if self.sleep_between_channels != -1:
                    sleep(self.sleep_between_channels)
        sensor_data = list()
        sensor_data = (self.guid, self.this_moment, self.daqChannels[0], self.daqChannels[1], self.daqChannels[2], self.daqChannels[3])
        print (sensor_data)
        return sensor_data

    def closeDaq(self):
        pass


class ADS1115Stream(DaqStream):
    daq_info = None
    gain = None
    stream_info_dict = {0:6.144, 1:4.096, 2:2.048, 4:1.024, 8:0.512, 16:0.256}

    def __init__(self):
        dsi = DAQStreamInfo()
        self.daq_info = dsi.getConfig(ini_file_name)

    @staticmethod
    def getInstance():
        return ADS1115Stream()
        
    def openDaq(self):
        import Adafruit_ADS1x15
        
        sys.path.insert(1, '/home/pi/Documents/Code/PlantPlayground')
        from pi.ADS1115Runner import ADS1115Runner

        self.daqChannels = [0.0, 0.0, 0.0, 0.0]
        self.this_moment = datetime.datetime.now().strftime("%H:%M:%S:%f")

        #GAIN = 16
        self.gain = int(self.daq_info.gain)
        self.data_rate = int(self.daq_info.data_rate) # 8, 16, 32, 64, 128, 250, 475, 860

        ads1115Runner = ADS1115Runner()
        self.adc = Adafruit_ADS1x15.ADS1115()
        
        # General settings        
        self.sleep_between_reads = int(self.daq_info.sleep_between_reads)
        # -1 = don't give away the time slice
        self.sleep_between_channels = float(self.daq_info.sleep_between_channels)
        self.number_of_channels = int(self.daq_info.number_of_channels)
        self.channels = self.daq_info.channels #[True, True, True, True] #self.daq_info.channels #[True, True, True, True] #self.daq_info.channels #
        #self.ads1115_sensor_type = 'differential_value_read' #'single_value_read' # 'differential_value_read'
        self.ads1115_sensor_type = self.daq_info.ads1115_sensor_type
        assert (self.ads1115_sensor_type == 'differential_value_read')
        ####
        self.low_chan = int(self.daq_info.low_chan)
        self.high_chan = int(self.daq_info.high_chan)

        self.guid = getGUID()

    def readDaq(self):
        if self.sleep_between_reads != -1:
            sleep(self.sleep_between_reads)
        self.this_moment = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S:%f")
        for ch in range(self.low_chan, self.high_chan + 1):
            if self.channels[ch] is True:
                if (self.ads1115_sensor_type == 'single_value_read'):         
                    self.daqChannels[ch] = self.adc.read_adc(ch, self.gain, self.data_rate)
                elif (self.ads1115_sensor_type == 'differential_value_read'):
                    adc_reading = self.adc.read_adc_difference(ch, self.gain, self.data_rate)
                    self.voltsPerDivision = ((2 * self.stream_info_dict[self.gain])/65535)*1000
                    self.daqChannels[ch] = adc_reading * self.voltsPerDivision
                if self.sleep_between_channels != -1:
                    sleep(self.sleep_between_channels)
        sensor_data = list()
        sensor_data = (self.guid, self.this_moment, self.daqChannels[0], self.daqChannels[1], self.daqChannels[2], self.daqChannels[3])
        print ("ADS1115Stream sensor data: " + str(sensor_data))
        return sensor_data

    def closeDaq(self):
        pass


class ADS1115i2cStream(DaqStream):
    import smbus2, RPi.GPIO as GPIO
    import Adafruit_ADS1x15
    
    sys.path.insert(1, '/home/pi/Documents/Code/PlantPlayground')
    from pi.ADS1115Runner import ADS1115Runner

    sys.path.insert(1, '/home/pi/grove.py/')
    #from grove.adc import ADC

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
    daq_info = None
    gain = None
    stream_info_dict = {0:6.144, 1:4.096, 2:2.048, 4:1.024, 8:0.512, 16:0.256}

    def __init__(self):
        dsi = DAQStreamInfo()
        self.daq_info = dsi.getConfig(ini_file_name)

    @staticmethod
    def getInstance():
        return ADS1115i2cStream()

    def openDaq(self):
        self.daqChannels = [0.0, 0.0, 0.0, 0.0]
        self.this_moment = datetime.datetime.now().strftime("%H:%M:%S:%f")

        #GAIN = 16
        self.gain = int(self.daq_info.gain)
        self.data_rate = int(self.daq_info.data_rate) # 8, 16, 32, 64, 128, 250, 475, 860

        # General settings        
        self.sleep_between_reads = int(self.daq_info.sleep_between_reads)
        # -1 = don't give away the time slice
        self.sleep_between_channels = float(self.daq_info.sleep_between_channels)
        self.number_of_channels = int(self.daq_info.number_of_channels)
        self.channels = self.daq_info.channels #[True, True, True, True] #self.daq_info.channels #[True, True, True, True] #self.daq_info.channels #
        #self.ads1115_sensor_type = 'differential_value_read' #'single_value_read' # 'differential_value_read'
        self.ads1115_sensor_type = self.daq_info.ads1115_sensor_type
        self.low_chan = int(self.daq_info.low_chan)
        self.high_chan = int(self.daq_info.high_chan)
        self.guid = getGUID()
        
        sys.path.insert(1, '/home/pi/Documents/Code/PlantPlayground')
        from pi.ADS1115Runner import ADS1115Runner

        self.sensor = 0
        #self.voltsPerDivision = ((2 * self.adcInfo.volts_per_division_table[self.gain])/65535)*1000
        # Open for differential_i2c
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
        return #self.channel

    def readDaq(self):
        if self.sleep_between_reads != -1:
            sleep(self.sleep_between_reads)
        self.this_moment = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S:%f")
        for ch in range(self.low_chan, self.high_chan + 1):
            if self.channels[ch] is True:
                if (self.ads1115_sensor_type == 'single_value_read'):         
                    self.daqChannels[ch] = self.ads1115Runner.i2c_read(ch) #self.adc.read_adc(ch, self.gain, self.data_rate)
                elif (self.ads1115_sensor_type == 'differential_value_read'):
                    adc_reading = self.ads1115Runner.i2c_read(ch) #self.adc.read_adc_difference(ch, self.gain, self.data_rate)
                    self.voltsPerDivision = ((2 * self.stream_info_dict[self.gain])/65535)*1000
                    self.daqChannels[ch] = adc_reading * self.voltsPerDivision
                if self.sleep_between_channels != -1:
                    sleep(self.sleep_between_channels)
        sensor_data = list()
        sensor_data = (self.guid, self.this_moment, self.daqChannels[0], self.daqChannels[1], self.daqChannels[2], self.daqChannels[3])
        print ("ADS1115i2cStream sensor data: " + str(sensor_data))
        return sensor_data

        #if (self.reader_type == 'differential_i2c'):
        #self.value_raw = self.ads1115Runner.i2c_read(channel)
        #return self.value_raw #* self.voltsPerDivision

    def closeDaq(self):
        pass

class ADS1256Stream(DaqStream):

    @staticmethod
    def getInstance():
        return ADS1256Stream()

    def openDaq(self):
        super().openDaq()
        #print("ADS1256Stream Open...")

        import time
        import RPi.GPIO as GPIO

        # ADS1256 Specific Setting
        sys.path.insert(1, '/home/pi/Documents/Code/PlantPlayground')
        import pi.ADS1256 as ADS1256
        self.ADC = ADS1256.ADS1256()
        self.ADC.ADS1256_init()
        self.gain = int(self.daq_info.gain)
        self.data_rate = int(self.daq_info.data_rate) # 8, 16, 32, 64, 128, 250, 475, 860
        self.ADC.ADS1256_ConfigADC(self.gain, self.data_rate)
        
        self.scan_mode = int(self.daq_info.scan_mode)
        self.ADC.ADS1256_SetMode(self.scan_mode)
        if(self.scan_mode == 0):
            for i in range(0, self.daq_info.number_of_channels):
                self.ADC.ADS1256_SetChannal(i)
        elif(self.scan_mode == 1):
            for i in range(0, self.number_of_channels):
                self.ADC.ADS1256_SetDiffChannal(i)
                
        self.daq_method = self.ADC.ADS1256_GetChannalValue
        self.conversion_method = self.no_conversion
                                 
    def no_conversion(self) -> int:
        return 1
                
    def closeDaq(self):
        pass



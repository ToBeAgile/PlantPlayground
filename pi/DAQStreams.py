# DAQStreams.py 1.0 - May 8, 2022 - June 19, 2022 (c)reated by David Scott Bernstein
# DAQStreams.py - Supports multiple DAQs, called by PPRemote.py
# Supported DAQs: ADS1256, MCC128, ADS1115, ADS1115i2c
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
        
    @abstractmethod
    # This method is abstract because a subclass must define and return a daq_method that readDaq will call
    def openDaq(self) -> callable:
        # General settings        
        self.number_of_channels = self.daq_info.number_of_channels
        self.daqChannels = [0.0, 0.0, 0.0, 0.0]
        self.sleep_between_reads = int(self.daq_info.sleep_between_reads)
        self.sleep_between_channels = float(self.daq_info.sleep_between_channels)
        self.number_of_channels = int(self.daq_info.number_of_channels)
        self.channels = self.daq_info.channels
        #self.ads1256_sensor_type = self.daq_info.ads1256_sensor_type
        self.low_chan = int(self.daq_info.low_chan)
        self.high_chan = int(self.daq_info.high_chan)
        
        try:
            # Ensure low_chan and high_chan are valid.
            if self.low_chan < 0 or self.low_chan >= self.number_of_channels:
                error_message = ('Error: Invalid low_chan selection - must be '
                                 '0 - {0:d}'.format(self.number_of_channels - 1))
                raise Exception(error_message)
            if self.high_chan < 0 or self.high_chan >= self.number_of_channels:
                error_message = ('Error: Invalid high_chan selection - must be '
                                 '0 - {0:d}'.format(self.number_of_channels - 1))
                raise Exception(error_message)
            if self.low_chan > self.high_chan:
                error_message = ('Error: Invalid channels - high_chan must be '
                                 'greater than or equal to low_chan')
                raise Exception(error_message)
        except:
            print('Channel setup error...')
            
        self.guid = getGUID()
        self.this_moment = datetime.datetime.now().strftime("%H:%M:%S:%f")
    
    # This generic read works for any DAQ by passing in the daq_method() to use
    # This function pointer is returned by the the subclasses openDaq method and passed into this method to call
    def readDaq(self, daq_method):
        if self.daq_info.sleep_between_reads != -1:
            sleep(self.daq_info.sleep_between_reads)
        self.this_moment = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S:%f")
        for ch in range(self.daq_info.low_chan, self.daq_info.high_chan + 1):
            if self.daq_info.channels[ch] is True:
                self.daqChannels[ch] =  daq_method(ch)
                if self.daq_info.sleep_between_channels != -1:
                    sleep(self.daq_info.sleep_between_channels)
        sensor_data = list()
        sensor_data = (self.guid, self.this_moment, self.daqChannels[0], self.daqChannels[1], self.daqChannels[2], self.daqChannels[3])
        print (str(sensor_data))
        return sensor_data

    def closeDaq(self):
        pass

class ADS1256Stream(DaqStream):

    @staticmethod
    def getInstance():
        return ADS1256Stream()

    def openDaq(self) -> callable:
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
        self.sensor_type = self.daq_info.sensor_type
        
        if self.sensor_type == 'single_ended':
            self.scan_mode = 0
        else: # sensor_type defaults to differntial
            self.scan_mode = 1
        self.ADC.ADS1256_SetMode(self.scan_mode)
        if(self.scan_mode == 0): # Single_ended mode
            for i in range(0, self.daq_info.number_of_channels):
                self.ADC.ADS1256_SetChannal(i)
        elif(self.scan_mode == 1): # Differential mode
            for i in range(0, self.number_of_channels):
                self.ADC.ADS1256_SetDiffChannal(i)
                
        self.daq_method = self.ADC.ADS1256_GetChannalValue
        self.conversion_method = self.no_conversion
        return (self.daq_method)
                                 
    def no_conversion(self) -> int: 
        return 1
                
    def closeDaq(self):
        pass
    

class MCC128Daq(DaqStream):
    
    def openDaq(self):
        from daqhats import mcc128, OptionFlags, HatIDs, HatError, AnalogInputMode, \
            AnalogInputRange
        from daqhats_utils import select_hat_device, enum_mask_to_string, \
            input_mode_to_string, input_range_to_string
        # MCC128-specific settings
        self.analog_input_range = self.daq_info.analog_input_range
        #assert( self.analog_input_range == 'AnalogInputRange.BIP_10V')
        #self.reader_type = 'differential'  # or 'single-ended'
        self.reader_type = self.daq_info.reader_type
        self.options = self.daq_info.options
        self.input_mode = AnalogInputMode.DIFF
        #self.input_mode = daq_info.input_mode #AnalogInputMode.DIFF  # or SE
        if(self.daq_info.options == 'AnalogInputMode.DIFF'):
            self.input_mode = AnalogInputMode.DIFF
        elif(self.daq_info.options == AnalogInputMode.SE):
            self.input_mode = AnalogInputMode.SE
        #self.daq_info.input_range #AnalogInputRange.BIP_10V
        self.input_range = AnalogInputRange.BIP_10V 
        if (self.daq_info.input_range == AnalogInputRange.BIP_10V):    
            self.input_range = AnalogInputRange.BIP_10V  # BIP_1V
        elif (self.daq_info.input_range == AnalogInputRange.BIP_1V):
            self.input_range = AnalogInputRange.BIP_1V  # BIP_10V
        self.sample_interval = self.daq_info.sample_interval #0.1  # 0.5  # Seconds
        self.number_of_channels = self.daq_info.number_of_channels #mcc128.info().NUM_AI_CHANNELS[self.input_mode]
        self.myHatError = HatError
        # Get an instance of the selected hat device object.
        address = select_hat_device(HatIDs.MCC_128)
        self.hat = mcc128(address)

        self.hat.a_in_mode_write(self.input_mode)
        self.hat.a_in_range_write(self.input_range)
        self.sensor = self.hat
        
        self.daq_method = self.hat.a_in_read
        self.conversion_method = self.no_conversion
        return self.daq_method
                                 
    def no_conversion(self) -> int:
        return 1
    
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
        
    def openDaq(self) -> callable:
        #super().openDaq()

        import Adafruit_ADS1x15
        
        sys.path.insert(1, '/home/pi/Documents/Code/PlantPlayground')
        from pi.ADS1115Runner import ADS1115Runner

        self.daqChannels = [0.0, 0.0, 0.0, 0.0]
        self.this_moment = datetime.datetime.now().strftime("%H:%M:%S:%f")

        self.gain = int(self.daq_info.gain)
        self.data_rate = int(self.daq_info.data_rate) # 8, 16, 32, 64, 128, 250, 475, 860

        ads1115Runner = ADS1115Runner()
        self.adc = Adafruit_ADS1x15.ADS1115()
        
        self.guid = getGUID()
        
        if (self.daq_info.sensor_type == 'single_ended'):         
            self.daq_method = self.adc.read_adc #(ch, self.gain, self.data_rate)
        else:
            self.daq_method = self.adc.read_adc_difference #(ch, self.gain, self.data_rate)

        self.conversion_method = self.convert_to_volts
        #print("daq_method: " + str(self.daq_method))
        return self.daq_method
                                 
    def convert_to_volts(self) -> int:
        voltsPerDivision = ((2 * self.stream_info_dict[self.gain])/65535)*1000
        return voltsPerDivision
                
    def closeDaq(self):
        pass

#CLASSES: ADS1115i2cSingleEnded, ADS1115i2cDifferential
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

        self.gain = int(self.daq_info.gain)
        self.data_rate = int(self.daq_info.data_rate) # 8, 16, 32, 64, 128, 250, 475, 860
        sys.path.insert(1, '/home/pi/Documents/Code/PlantPlayground')
        from pi.ADS1115Runner import ADS1115Runner

        self.sensor = 0
        #self.voltsPerDivision = ((2 * self.adcInfo.volts_per_division_table[self.gain])/65535)*1000
        # Open for differential_i2c
        config_string = '1-000-111-1-000-0-0-0-11'
        self.ads1115Runner.i2c_reader_init(config_string)
        #adc = ADCStreamReader()
        #resetChip()
        # compare with configuration settings from ADS115 datasheet
        # start single conversion - AIN2/GND - 4.096V - single shot - 8SPS - X
        # - X - X - disable comparator
        #conf = prepareLEconf('1-000-111-1-100-1-0-0-11')
        #conf = prepareLEconf('0-000-111-1-100-1-0-0-11')
        self.guid = getGUID()
        
        if (self.daq_info.sensor_type == 'single_ended'):         
            self.daq_method = self.ads1115Runner.i2c_read #self.adc.read_adc #(ch, self.gain, self.data_rate)
        else:
            self.daq_method = self.ads1115Runner.i2c_read #(ch, self.gain, self.data_rate)

        self.conversion_method = self.convert_to_volts
        #print("daq_method: " + str(self.daq_method))
        return self.daq_method
                                 
    def convert_to_volts(self) -> int:
        voltsPerDivision = ((2 * self.stream_info_dict[self.gain])/65535)*1000
        return voltsPerDivision

    def closeDaq(self):
        pass



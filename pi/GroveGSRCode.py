#GroveGSR code

#GroveGSR Sensor
class GroveGSRStream(DaqStream):
    import smbus2, RPi.GPIO as GPIO
    import Adafruit_ADS1x15
    
    sys.path.insert(1, '/home/pi/grove.py/')
    from grove.adc import ADC

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

    #ads1115Runner = ADS1115Runner()
    #adc = Adafruit_ADS1x15.ADS1115()
    #DaqInfo = DaqStreamInfo()
    
    #ip = "127.0.0.1"
    #port = 1337
    #daq = MCC128Daq()
    #client = SimpleUDPClient(ip, port)  # Create client

    def __init__(self):
       #self.channel = channel
        pass

    @staticmethod
    def getInstance():
        return GroveGSRStream()

    def openDaq(self):
        self.Daq = ADC()
        self.sensor = GroveGSRSensor(int(0))
        return self.channel
    
    def readDaq(self):
        time.sleep(self.sleep)            
        return self.sensor.GSR

    def closeDaq(self):
        pass



# Constants
#CURSOR_BACK_2 = '\x1b[2D'
#ERASE_TO_END_OF_LINE = '\x1b[0K'


class GroveGSRSensor:
    sys.path.insert(1, '/home/pi/grove.py/')
    from grove.adc import ADC
    
    def __init__(self, channel):
        self.channel = channel
        self.Daq = ADC()

    @property
    def GSR(self):
        value = self.adc.read(self.channel)
        return value
    
'''
#the old way of doing things
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
    #DaqInfo = DaqStreamInfo()
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
'''
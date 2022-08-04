# DAQStreamInfo.py 1.0 - May 23, 2022 - June 19, 2022 (c)reated by David Scott Bernstein
# DAQStreamInfo.py - config file handling called by DAQStreams.py
import configparser
import ast

ini_file_name = 'DAQStreams.ini'

class DAQStreamInfo:

    def __init__(self):
        self.daq_to_use = None
        self.sensor_type = None
        self.sensor_read_frequency = None
        self.number_of_channels = None
        self.data_log_frequency = None
        self.sensor_read_frequency = None
        self.network_write_frequency = None
        self.to_log = None
        ###
        self.sleep_between_reads = None
        sleep_between_channels = None
        number_of_channels = None
        low_chan = None
        high_chan = None
        channels = []
        sensor_type = None
        ###
        self.analog_input_range = None
        self.reader_type = None
        self.options = None
        self.input_mode = None
        self.input_range = None
        self.daq = None
        self.device = None
        self.num_channels = None
        self.hat_error = None
        self.sample_interval = 0.0
        ###
        self.gain = None
        self.data_rate = None
        self.scan_mode = 0
        ###
        self.dac1_frequency = 0
        self.dac1_sample_rate = 0
        self.dac1_interval = 0
        self.dac2_frequency = 0
        self.dac2_sample_rate = 0
        self.dac2_interval = 0
        

    def getConfig(self, ini_file_name):
        config = configparser.ConfigParser()
        config.read(ini_file_name)
        # General settings
        self.daq_to_use = config['Default']['daq_to_use']
        #self.ads1115_sensor_type = config['Default']['ads1115_sensor_type']
        self.number_of_channels = config['Default']['number_of_channels']
        self.data_log_frequency = float(config['Default']['data_log_frequency'])
        self.sensor_read_frequency = config['Default']['sensor_read_frequency']
        self.network_write_frequency = config['Default']['network_write_frequency']
        self.to_log = config['Default']['to_log']
        ###
        self.sleep_between_reads = float(config['Default']['sleep_between_reads'])
        self.sleep_between_channels = float(config['Default']['sleep_between_channels'])
        self.number_of_channels = int(config['Default']['number_of_channels'])
        self.low_chan = int(config['Default']['low_chan'])
        self.high_chan = int(config['Default']['high_chan'])
        self.channels = ast.literal_eval(config.get('Default', 'channels'))
        self.sensor_type = config['Default']['sensor_type']
        #MCC128 specific
        self.analog_input_range = config['Default']['analog_input_range']
        self.reader_type = config['Default']['reader_type']
        self.options = config['Default']['options']
        self.input_mode = config['Default']['mcc_input_mode']
        self.input_range = config['Default']['input_range']
        self.daq = config['Default']['DAQ']
        self.device = config['Default']['Device']
        self.num_channels = config['Default']['NumChannels']
        self.hat_error = config['Default']['mcc_hat_error']
        self.gain = config['Default']['gain']
        self.data_rate = config['Default']['data_rate']
        ###ADS1256 specific
        self.dac1_frequency = config['Default']['dac1_frequency']
        self.dac1_sample_rate = config['Default']['dac1_sample_rate']
        self.dac1_interval = config['Default']['dac1_interval']
        self.dac2_frequency = config['Default']['dac2_frequency']
        self.dac2_sample_rate = config['Default']['dac2_sample_rate']
        self.dac2_interval = config['Default']['dac2_interval']
        
        return self

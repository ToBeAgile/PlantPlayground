# PPRemote.py - Remote Data Aquisition, Logger, and network broadcaster
''' Next:
Read DAQ settings from config file, implement other DAQs
Move unneeded files from pi to a backup area
Read all settings from config file, pass needed ones to DAQStreams
Get single_ended and differential reads working on ADS1115
Copy code from ASD1115 to i2C 
Clean up code, deleted unneeded lines
Get logging working 
Get logging headers working 
Get second DAQ working
'''
import socket
import sys
import time
import pickle
import random
import datetime
import threading
import csv
import os.path
import unittest
import configparser

sys.path.insert(1, '/home/pi/Documents/Code/PlantPlayground')
from pi.DAQStreams import *

ini_file_name = 'DAQStreams.ini'

class DAQStreamInfo():

    def __init__(self):
        self.daq_to_use = None
        self.single_ended_or_differential = None
        self.sensor_read_frequency = None
        self.number_of_channels = None
        self.data_log_frequency = None
        self.sensor_read_frequency = None
        self.network_write_frequency = None
        self.to_log = None
        self.sleep_between_reads = None
        ###
        self.analog_input_range = None
        self.reader_type = None
        self.options = None
        self.input_mode = None
        self.input_range = None
        self.daq = None
        self.device = None
        self.num_channels = None

    def getConfig(self, ini_file_name):
        config = configparser.ConfigParser()
        config.read(ini_file_name)
        # General settings
        self.daq_to_use = config['Default']['daq_to_use']
        self.single_ended_or_differential = config['Default']['single_ended_or_differential']
        self.number_of_channels = config['Default']['number_of_channels']
        self.data_log_frequency = int(config['Default']['data_log_frequency'])
        self.sensor_read_frequency = config['Default']['sensor_read_frequency']
        self.network_write_frequency = config['Default']['network_write_frequency']
        self.to_log = config['Default']['to_log']
        self.sleep_between_reads = config['Default']['sleep_between_reads']
        self.analog_input_range = config['Default']['analog_input_range']
        self.reader_type = config['Default']['reader_type']
        self.options = config['Default']['options']
        self.input_mode = config['Default']['input_mode']
        self.input_range = config['Default']['input_range']
        self.daq = config['Default']['DAQ']
        self.device = config['Default']['Device']
        self.num_channels = config['Default']['NumChannels']
        return self
''' put in DaqStreamInfo and pass to ADCStreamReader
sleep_between_reads = -1  # -1 = don't give away the time slice
sleep_between_channels = 0.25
number_of_channels = 4
low_chan = 0
high_chan = 3
channels = [True, True, True, True]
sensor_type = 'mcc_single_value_read'
reader_type_a = 'mcc_single_value_read'  # 'grove_gsr' # 'dummy_read' #'single_ended' #'differential_i2c' #'single_ended' #'differential'
reader_type_b = 'mcc_single_value_read'  # 'grove_gsr' # 'dummy_read' #'single_ended' #'differential_i2c' #'single_ended' #'differential'
'''

'''
a_gain = 1 #16
b_gain = 1 #16
a_data_rate = 128
b_data_rate = 128
volts_per_division_table = {2/3:6.144, 1:4.096, 2:2.048, 4:1.024, 8:0.512, 16:0.256}
a_mv_per_division = ((2 * volts_per_division_table[a_gain])/65535)*1000
b_mv_per_division = ((2 * volts_per_division_table[b_gain])/65535)*1000
sensor_state = 0
channel0 = 0
channel1 = 1
chan = 0
'''
#Initialize the shared variables across threads
"""
a_raw_value = 1 #adc.read_adc_difference(0, gain=a_gain, data_rate=a_data_rate)
a_value = a_raw_value * a_mv_per_division
a_time = datetime.datetime.now()
time.sleep(0.01)
b_raw_value = 1 #adc.read_adc_difference(3, gain=b_gain, data_rate=b_data_rate)
b_value = b_raw_value * b_mv_per_division
b_time = datetime.datetime.now()
daq_data = 1
"""


def read_sensor():
    global daq_data
    #Calculated from settings read in from config file
    sensor_read_time = float(1/float(0.1)) #(dsi.sensor_read_frequency))
    network_write_time = float(1/float(10)) #(dsi.network_write_frequency))
    data_log_time = float(1/float(1)) #(dsi.data_log_frequency))

    #adc = DaqStream.getInstance()
    #adc = ADS1115Stream()
    #adc = DaqStreamTester()
    
    # Determine which DAQ to use
    daq_info = DAQStreamInfo().getConfig(ini_file_name) #get reading from ini file to work
    #print(daq_info.daq_to_use)
    #adc = ADS1115Stream()
    #daq_info.daq_to_use = 'ADS1115Stream'
    #print(daq_info.daq_to_use)

    if (daq_info.daq_to_use == '\'MCC128Daq\''):
        adc = MCC128Daq()
    elif (daq_info.daq_to_use == '\'ADS1115Stream\''):
        adc = ADS1115Stream()
    elif (daq_info.daq_to_use == '\'ADS1115i2cStream\''):
        adc = ADS1115i2cStream()
    else:
        adc = ADS1115i2cStream()
        
    adc.openDaq()
    
    while True:
        daq_data = adc.readDaq()
        #print(daq_data)
        #if DaqInfo.sleep_between_reads != -1:
        #    sleep(DaqInfo.sleep_between_reads)
'''            
        if (number_of_channels > 1):
            b_raw_value = adc.read(channel1)
            b_value = b_raw_value * b_mv_per_division
            b_time = datetime.datetime.now().strftime("%H:%M:%S:%f")
 '''

        #b_raw_value = adc.read_adc_difference(3, gain=b_gain, data_rate=860)
        #b_value = (adc.read_adc_difference(3, gain=b_gain, data_rate=b_data_rate)) * b_mv_per_division
        #b_raw_value = adc.read(channel1)
        #b_value = b_raw_value * b_mv_per_division
        #b_time = datetime.datetime.now().strftime("%H:%M:%S:%f")  
        #print("Channel A: ", a_time, a_raw_value, a_value, " Channel B: ", b_time, b_raw_value, b_value)        
        #read_event.wait(sensor_read_time) #todo depend on a user modified variable
 
def write_network():
    global daq_data

    #set up the network connection
    host =  '192.168.4.39' # was '192.168.0.18' '127.0.1.1' #
    port = 50000

    s = None
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))

    except socket.error as message:
        if s:
            s.close()
        print ("Unable to open the socket: " + str(message))
        sys.exit(1)

    while True:
        write_event.wait(network_write_time)
        data_dict = daq_data
        print(data_dict)
        serialized_data = pickle.dumps(data_dict)
        s.send(serialized_data)


def log_data():
    global daq_data

    now = datetime.datetime.now()
    folder_name = "..//data//"
    project_code = "R0"
    file_name = project_code + "-" + now.strftime("%Y-%m-%d") + ".csv"
    full_path = folder_name + file_name
    #file = open(full_path, 'a', newline='', buffering=1)
    to_log = False #put into config
    if (to_log == False):
        return
    
    if os.path.isfile(full_path):
        #with open(full_path, 'a', newline='', buffering=1) as file:
            #writer = csv.writer(file)
        file = open(full_path, 'a', newline='', buffering=1)
        writer = csv.writer(file)
    else:
        #with open(full_path, 'w', newline='', buffering=1) as file:
        file = open(full_path, 'w', newline='', buffering=1)            
        writer = csv.writer(file)
        #writer and write the header
        writer.writerow(["Plant bioelectric data log by David Scott Bernstein. Project: Setup, File name: " + file_name])
        writer.writerow(["Software: PlantPlayground, File: PP-Remote.py, Version 0.2"])
        #writer.writerow(["Reading 2 differential channels in milivolts with a sensor read frequency of " + str(sensor_read_time) + "."])
        #writer.writerow(["Reading 4 channel(s) in milivolts with a sensor read frequency of " + str(sensor_read_time) + "."])
        #writer.writerow(["Channel B is connected to nothing, Channel A is connected my old Op Amp from 35 years ago and then to a plant."])
        #writer.writerow(["The plant is in a Faraday cage and the Pi 4 is in a Faraday cage inside the Faraday cage with a common ground."])
        #writer.writerow(["Gain: " + str(a_gain) + ", Data Rate: " + str(a_data_rate) + ", Volts per Division: " + str(a_mv_per_division) + "."])
        #writer.writerow(["Channels A and B are connected using a silver-silver chloride wire that I made myself."])
        #writer.writerow(["Gain: " + str(b_gain) + ", Data Rate: " + str(b_data_rate) + ", Volts per Division: " + str(b_mv_per_division) + "."])
        #writer.writerow(["Channel A Open Type: " + reader_type_a + "Channel B Open Type: " + reader_type_b + "."])

    while True:
        log_event.wait(data_log_time)
        #print(daq_data)
        writer.writerow(daq_data)

        #writer.writerow(["Channel A: " + str(a_time) + ", " + str(a_raw_value) + ", " + str(a_value)
                         #+ '; Channel B: ' + str(b_time) + ", " + str(b_raw_value) + ", " + str(b_value)])
    file.close()

read_event = threading.Event()
write_event = threading.Event()
log_event = threading.Event()
#floats, ints, and dictionaries should all be thread safe in Python (floats and ints are immutable). Test this
threading.Thread(target=read_sensor).start()
threading.Thread(target=write_network).start()
threading.Thread(target=log_data).start()

#class GettingStartedTest(unittest.TestCase):
#    def test_simple(self):
#        verify("Hello ApprovalTests")

#if __name__ == "__main__":
#    unittest.main()
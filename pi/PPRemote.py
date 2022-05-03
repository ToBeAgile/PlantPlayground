# PPRemote.py - Remote Data Aquisition, Logger, and network broadcaster
''' Next:
Move unneeded files from pi to a backup area
Do single-ended and differential reads on ASD1115i2C
Get new DAQ working
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

sys.path.insert(1, '/home/pi/Documents/Code/PlantPlayground/pi')
from DAQStreams import *

ini_file_name = 'DAQStreams.ini'
global daq_data
    
def read_sensor():
    #Calculated from settings read in from config file
    #sensor_read_time = float(1/float(0.1)) #(dsi.sensor_read_frequency))
    #network_write_time = float(1/float(10)) #(dsi.network_write_frequency))
    #data_log_time = float(1/float(1)) #(dsi.data_log_frequency))
    
    # Determine which DAQ to use
    adc = DaqStream.getInstance()
    adc.openDaq()
    
    while True:
        daq_data = adc.readDaq()
        
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
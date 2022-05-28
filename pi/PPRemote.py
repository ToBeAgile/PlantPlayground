# PPRemote.py 1.0 - May 8, 2022 (c)reated by David Scott Bernstein
# PPRemote.py - Remote Data Aquisition, Logger, and network broadcaster

''' Next:
Get all channels on ASDS1256 working
Verify readings from ADS1256 using potentimeter
Clean up loggin headers

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
#global daq_data
daq_data = list()

dsi = DAQStreamInfo()
daq_info = dsi.getConfig(ini_file_name)

def read_sensor():
    global daq_data
    #Calculated from settings read in from config file
    #sensor_read_time = float(1/float(0.1)) #(dsi.sensor_read_frequency))
    #network_write_time = float(1/float(10)) #(dsi.network_write_frequency))
    #data_log_time = float(1/float(1)) #(dsi.data_log_frequency))
    
    # Determine which DAQ to use
    adc = DaqStream.getInstance()
    adc.openDaq()
    
    while True:
        daq_data = adc.readDaq()
        #update to pass functions for read and convert to mV
        #print(daq_data)
 
#fix this by comparing to early working version
def write_network():
    global daq_data
    #set up the network connection
    host =  '192.168.4.39' #'192.168.4.39' # was '192.168.0.18' '127.0.1.1' #'192.168.0.4' #
    port = 50000
    #print("going into write network...")
    s = None
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("waiting for host...")
        s.connect((host, port))
        print("Connected...")
    except socket.error as message: 
        if s:
            s.close()
        print ("Unable to open the socket: " + str(message))
        sys.exit(1)

    while True:
        write_event.wait(1) #network_write_time)
        data_dict = daq_data
        print('helloww')#data_dict)
        serialized_data = pickle.dumps(data_dict)
        s.send(serialized_data)


def log_data():
    global daq_data
    if (daq_info.to_log == False):
        return
    
    now = datetime.datetime.now()
    folder_name = "../data/"
    project_code = "R0"
    file_name = project_code + "-" + now.strftime("%Y-%m-%d") + ".csv"
    full_path = folder_name + file_name
    
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
        writer.writerow(['Plant bioelectric data log: Setup, File name: ' + file_name])
        writer.writerow(['Software: PlantPlayground, File: PPRemote.py, Version 0.4'])
        #do we want to create another file with the same GUID with details about the session?
        #what info do we want? DAQs? number of channels? gain? sample rate? etc.
        #write sub-header from file
        writer.writerow(['GUID,Time,Ch0,ch1,ch2,ch3'])

    while True:
        #log_event.wait(data_log_time)
        sleep(daq_info.data_log_frequency)
        #print(daq_data)
        writer.writerow(daq_data)

    file.close()

read_event = threading.Event()
write_event = threading.Event()
log_event = threading.Event()
#floats, ints, and dictionaries should all be thread safe in Python (floats and ints are immutable). Test this
threading.Thread(target=read_sensor).start()
threading.Thread(target=write_network).start()
if (daq_info.to_log == 'True'):
    threading.Thread(target=log_data).start()

#class GettingStartedTest(unittest.TestCase):
#    def test_simple(self):
#        verify("Hello ApprovalTests")

#if __name__ == "__main__":
#    unittest.main()
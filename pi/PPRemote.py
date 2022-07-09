# PPRemote.py 1.0 - May 8, 2022 - June 19, 2022 (c)reated by David Scott Bernstein
# PPRemote.py - Remote Data Aquisition, Logger, and network broadcaster

''' Next:
Move GUID in header of log and out of each line
Verify readings from ADS1256 using potentimeter
Design impedence spectroscopy system:
    Write sin wave element, read DAQ channel and store in array

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

def getGUID():
    id = uuid.uuid4()
    return id.hex

def read_sensor():
    global daq_data
    #daq_method: callable

    # Determine which DAQ to use
    adc = DaqStream.getInstance()
    daq_method = adc.openDaq()
    
    while True:
        daq_data = adc.readDaq(daq_method)

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

def get_file_name() -> str:
    now = datetime.datetime.now()
    folder_name = "../data/"
    project_code = "R0"
    file_name = project_code + "-" + now.strftime("%Y-%m-%d") + ".csv"
    full_path = folder_name + file_name
    return full_path

def append_to_existing_file():
    #with open(full_path, 'a', newline='', buffering=1) as file:
    #writer = csv.writer(file)
    file = open(get_file_name(), 'a', newline='', buffering=1)
    writer = csv.writer(file)
    return writer

def open_new_file_and_write_header():
    _full_path = get_file_name()
    file = open(_full_path, 'w', newline='', buffering=1)            
    writer = csv.writer(file)
    #write the header with the GUID
    #'Data logger file: ' + file_name
    #'GUID: ' + guid
    writer.writerow(['Plant bioelectric data log: Setup, File name: ' + _full_path])
    writer.writerow(['Software: PlantPlayground, File: PPRemote.py, Version 1.0'])
    writer.writerow(['GUID: ' + getGUID() ]) #+ ', Created: ' + now.strftime("%Y-%m-%d")])
    #do we want to create another file with the same GUID containing details about the session?
    #what info do we want? DAQs? number of channels? gain? sample rate? etc.
    #write sub-header from file
    writer.writerow(['Time,Ch0,ch1,ch2,ch3'])
    return writer

def log_data():
    global daq_data
    if (daq_info.to_log == False):
        return
    
    full_path = get_file_name()
    if os.path.isfile(full_path):
        writer = append_to_existing_file()
    else:
        writer = open_new_file_and_write_header()

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

#if __name__ == "__main__":
#    unittest.main()
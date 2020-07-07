import socket
import sys
import time
import pickle
import random
import datetime
import Adafruit_ADS1x15
import threading
import csv
import os.path
#sys.path.insert(1, '.')
#from services.DataLogger import DataLogger
sys.path.insert(1, '/home/pi/Documents/Code/PlantPlayground')

#Set the rates. Implement these into a GUI
data_log_frequency = 0.01 #Hz  How many data points are logged each second locally, on the pi
sensor_read_frequency = 0.1 #0.1 #25 #Hz
network_write_frequency = 10 #10.0 #Hz    How many data points will be graphed each second

#Calculated from above
sensor_read_time = float(1/sensor_read_frequency)
network_write_time = float(1/network_write_frequency)
data_log_time = float(1/data_log_frequency)

# Create an ADS1115 ADC (16-bit) instance.
adc = Adafruit_ADS1x15.ADS1115()
a_gain = 16
b_gain = 16
a_data_rate = 128
b_data_rate = 128
volts_per_division_table = {2/3:6.144, 1:4.096, 2:2.048, 4:1.024, 8:0.512, 16:0.256}
a_mv_per_division = ((2 * volts_per_division_table[a_gain])/65535)*1000
b_mv_per_division = ((2 * volts_per_division_table[b_gain])/65535)*1000
sensor_state = 0

#Initialize the shared variables across threads
a_value = (adc.read_adc_difference(0, gain=a_gain, data_rate=a_data_rate)) * a_mv_per_division
a_time = datetime.datetime.now()
time.sleep(0.01)
b_value = (adc.read_adc_difference(3, gain=b_gain, data_rate=b_data_rate)) * b_mv_per_division
b_time = datetime.datetime.now()

#set up the network connection
host = '192.168.0.18'
port = 50000

s = None
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host,port))

except socket.error as message:
    if s:
        s.close()
    print ("Unable to open the socket: " + str(message))
    sys.exit(1)
    

def read_sensor():
    global a_value
    global a_time
    global b_value
    global b_time
    global sensor_state
    
    while True:
        #a_value = adc.read_adc_difference(0, gain=a_gain, data_rate=860)
        a_value = (adc.read_adc_difference(0, gain=a_gain, data_rate=a_data_rate)) * a_mv_per_division
        a_time = datetime.datetime.now().strftime("%H:%M:%S:%f")
        #b_value = adc.read_adc_difference(3, gain=b_gain, data_rate=860)
        b_value = (adc.read_adc_difference(3, gain=b_gain, data_rate=b_data_rate)) * b_mv_per_division
        b_time = datetime.datetime.now().strftime("%H:%M:%S:%f")
        print("Channel A: ", a_time, a_value, " Channel B: ", b_time, b_value)        
        read_event.wait(sensor_read_time) #todo depend on a user modified variable
 
def write_network():
    global a_value
    global a_time
    global b_value
    global b_time

    while True:
        write_event.wait(network_write_time)

        #write channel a
        data_dict = {"sensor": "a_sensor", "value": a_value, "time": a_time}
        #print(data_dict)
        serialized_data = pickle.dumps(data_dict)
        s.send(serialized_data)

        #write channel b
        data_dict = {"sensor": "b_sensor", "value": b_value, "time": b_time}
        serialized_data = pickle.dumps(data_dict)
        s.send(serialized_data)

def log_data():
    global a_value
    global a_time
    global b_value
    global b_time

    now = datetime.datetime.now()
    folder_name = "..//data//"
    project_code = "R0"
    file_name = project_code + "-" + now.strftime("%Y-%m-%d") + ".csv"
    full_path = folder_name + file_name
    #file = open(full_path, 'a', newline='', buffering=1)
    
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
        writer.writerow(["Software: PlantPlayground, File: PP-Remote.py, Version 0.1"])
        writer.writerow(["Reading 2 differential channels in milivolts with a sensor read frequency of " + str(sensor_read_time) + "."])
        writer.writerow(["The plant is in a Faraday cage and the Pi 4 is in a Faraday cage inside the Faraday cage with a common ground."])
        writer.writerow(["Channel A is connected to a potato in a Faraday cage. Channel B is connected to a plant in a Faraday cage."])
        writer.writerow(["Gain: " + str(a_gain) + ", Data Rate: " + str(a_data_rate) + ", Volts per Division: " + str(a_mv_per_division) + "."])
        writer.writerow(["Channels A and B are connected using a silver-silver chloride wire that I made myself."])
        writer.writerow(["Gain: " + str(b_gain) + ", Data Rate: " + str(b_data_rate) + ", Volts per Division: " + str(b_mv_per_division) + "."])

    while True:
        log_event.wait(data_log_time)
        writer.writerow(["Channel A: " + str(a_time) + ", " + str(a_value) + '; Channel B: ' + str(b_time) + ", " + str(b_value)])
    file.close()

read_event = threading.Event()
write_event = threading.Event()
log_event = threading.Event()
#floats, ints, and dictionaries should all be thread safe in Python (floats and ints are immutable). Test this
threading.Thread(target=read_sensor).start()
threading.Thread(target=write_network).start()
threading.Thread(target=log_data).start()

def a():
    return True


import socket
import sys
import time
import pickle
import random
import datetime
import Adafruit_ADS1x15
import threading
import csv
#sys.path.insert(1, '.')
#from services.DataLogger import DataLogger

#Set the rates. Implement these into a GUI
sensor_read_frequency = 20.0 #Hz
network_write_frequency = 10.0 #Hz    How many data points will be graphed each second
data_log_frequency = 0.01 #Hz  How many data points are logged each second locally, on the pi

#Calculated from above
sensor_read_time = float(1/sensor_read_frequency)
network_write_time = float(1/network_write_frequency)
data_log_time = float(1/data_log_frequency)

# Create an ADS1115 ADC (16-bit) instance.
adc = Adafruit_ADS1x15.ADS1115()
a_gain = 16
b_gain = 2/3
a_data_rate = 128
b_data_rate = 128
volts_per_division_table = {2/3:6.144, 1:4.096, 2:2.048, 4:1.024, 8:0.512, 16:0.256}
mv_per_division = ((2 * volts_per_division_table[a_gain])/65535)*1000
b_mv_per_division = ((2 * volts_per_division_table[b_gain])/65535)*1000
sensor_state = 0

#Initialize the shared variables across threads
a_value = (adc.read_adc_difference(0, gain=a_gain, data_rate=a_data_rate)) * mv_per_division
a_time = datetime.datetime.now()
time.sleep(0.01)
b_value = (adc.read_adc_difference(3, gain=b_gain, data_rate=b_data_rate)) * b_mv_per_division
b_time = datetime.datetime.now()

#set up the network connection
host = '192.168.1.5'
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
        #a_value = (adc.read_adc_difference(0, gain=a_gain, data_rate=a_data_rate)) * mv_per_division
        #a_time = datetime.datetime.now().strftime("%H:%M:%S:%f")
        
        
        if sensor_state == 0:
            a_value = (adc.read_adc_difference(0, gain=a_gain, data_rate=a_data_rate)) * mv_per_division
            a_time = datetime.datetime.now().strftime("%H:%M:%S:%f")
            sensor_state = sensor_state + 1
            #print("A time, value: ", a_time, a_value)
        elif sensor_state == 1:
            b_value = (adc.read_adc_difference(3, gain=b_gain, data_rate=b_data_rate)) * b_mv_per_division
            b_time = datetime.datetime.now().strftime("%H:%M:%S:%f")
            sensor_state = 0
            #print("B time, value: ", b_time, b_value)
        else:
            print("Sensor state machine error!")
            sensor_state = 0
        
        
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
    project_name = "R0"
    filename = project_name + "-" + now.strftime("%Y-%m-%d") + ".csv"
    #full_path = "/data/" + filename
    #with open(filename, 'a', newline='') as file:
    file = open(filename, 'a', newline='', buffering=1)
    writer = csv.writer(file)
    writer.writerow(["Plant bioelectric data log. Project: Setup"])
    writer.writerow(["Time", "Value"])
    #for k in range(10):
    while True:
        log_event.wait(data_log_time)
        writer.writerow([a_time, a_value])
    file.close()

read_event = threading.Event()
write_event = threading.Event()
log_event = threading.Event()
#floats, ints, and dictionaries should all be thread safe in Python (floats and ints are immutable). Test this
threading.Thread(target=read_sensor).start()
threading.Thread(target=write_network).start()
threading.Thread(target=log_data).start()

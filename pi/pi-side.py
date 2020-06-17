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
sensor_read_frequency = 25.0 #Hz
network_write_frequency = 20.0 #Hz    How many data points will be graphed each second
data_log_frequency = 2.0 #Hz  How many data points are logged each second locally, on the pi

#Calculated from above
sensor_read_time = float(1/sensor_read_frequency)
network_write_time = float(1/network_write_frequency)
data_log_time = float(1/data_log_frequency)

# Create an ADS1115 ADC (16-bit) instance.
adc = Adafruit_ADS1x15.ADS1115()
GAIN = 16
volts_per_division_table = {0:6.144, 1:4.096, 2:2.048, 4:1.024, 8:0.512, 16:0.256}
mv_per_division = ((2 * volts_per_division_table[GAIN])/65535)*1000

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
    

sensor = "CH0"
value = (adc.read_adc_difference(0, gain=GAIN, data_rate=128)) * mv_per_division
now = datetime.datetime.now()
sensor_time = now.strftime("%H:%M:%S:%f")


def read_sensor():
    global sensor
    global value
    global sensor_time

    #dl = DataLogger()

    while True:
        value = (adc.read_adc_difference(0, gain=GAIN, data_rate=128)) * mv_per_division
        now = datetime.datetime.now()
        sensor_time = now.strftime("%H:%M:%S:%f")
        #log the data
        #dl.write(str(time), str(value)) #this may be way too slow. Check implementation, might be reopening file every write. Even with a stream, might be too slow
        read_event.wait(sensor_read_time) #todo depend on a user modified variable

def write_network():
    global sensor
    global value
    global sensor_time

    while True:
        write_event.wait(network_write_time)
        #data_dict = {"sensor": sensor, "value": value, "time": sensor_time}
        #serialized_data = pickle.dumps(data_dict)
        serialized_data = pickle.dumps(value)
        s.send(serialized_data)

def log_data():
    global sensor
    global value
    global sensor_time

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
        writer.writerow([sensor_time, value])
    file.close()

read_event = threading.Event()
write_event = threading.Event()
log_event = threading.Event()
#floats, ints, and dictionaries should all be thread safe in Python (floats and ints are immutable). Test this
threading.Thread(target=read_sensor).start()
threading.Thread(target=write_network).start()
threading.Thread(target=log_data).start()

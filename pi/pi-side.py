import socket
import sys
import time
import pickle
import random
import datetime
import Adafruit_ADS1x15
import threading

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

    while True:
        value = (adc.read_adc_difference(0, gain=GAIN, data_rate=128)) * mv_per_division
        print(value)
        now = datetime.datetime.now()
        sensor_time = now.strftime("%H:%M:%S:%f")
        #time.sleep(.1) #todo depend on a user modified variable
        read_event.wait(0.4)

def write_network():
    global sensor
    global value
    global sensor_time

    while True:
        write_event.wait(1)
        print("Write: ", value)
        data_dict = {"sensor": sensor, "value": value, "time": sensor_time}
        serialized_data = pickle.dumps(data_dict)
        s.send(serialized_data)

read_event = threading.Event()
write_event = threading.Event()
#floats, ints, and dictionaries should all be thread safe in Python (floats and ints are immutable). Test this
threading.Thread(target=read_sensor).start()
threading.Thread(target=write_network).start()

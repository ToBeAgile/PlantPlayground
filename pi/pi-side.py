import socket
import sys
import time
import pickle
import random
import datetime
import Adafruit_ADS1x15

# Create an ADS1115 ADC (16-bit) instance.
adc = Adafruit_ADS1x15.ADS1115()
GAIN = 16
volts_per_division_table = {0:6.144, 1:4.096, 2:2.048, 4:1.024, 8:0.512, 16:0.256}
mv_per_division = ((2 * volts_per_division_table[GAIN])/65535)*1000

host = '192.168.1.14'
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
#value = random.randrange(-20, 20)
value = (adc.read_adc_difference(0, gain=GAIN, data_rate=128)) * mv_per_division
now = datetime.datetime.now()
sensor_time = now.strftime("%H:%M:%S:%f")

data_dict = {"sensor": sensor, "value": value, "time": sensor_time}
serialized_data = pickle.dumps(data_dict)

while True:
    value = (adc.read_adc_difference(0, gain=GAIN, data_rate=128)) * mv_per_division
    print(value)
    now = datetime.datetime.now()
    sensor_time = now.strftime("%H:%M:%S:%f")
    data_dict = {"sensor": sensor, "value": value, "time": sensor_time}
    serialized_data = pickle.dumps(data_dict)
    s.send(serialized_data)
    time.sleep(0.4)

s.close()

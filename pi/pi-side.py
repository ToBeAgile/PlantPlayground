#This is the side that will run on the pi. It should send data (lets have it send random data once a second)

import socket
import sys
import time
import pickle
import random #for testing
#sys.path.insert(1, '/home/pi/Documents/Code/PlantPlayground')
from ADCStreamReader import ADCStreamReader
import datetime

host = '192.168.0.18'
port = 50000

s = None
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host,port)) #remote server must already be running

except socket.error as message:
    if s:
        s.close()
    print ("Unable to open the socket: " + str(message))
    sys.exit(1)
    
adcSR = ADCStreamReader()
adc0 = adcSR.open(differential=0, gain=16, data_rate=8, sleep=0)

topic = "/PP01/ADC0/RAW/"

#data_dict = {"sensor": sensor, "value": value, "time": sensor_time}
#serialized_data = pickle.dumps(data_dict)

while True:
    #todo set the above sensor, dict, serialized_data, etc here
    #value = random.randrange(-20, 20)
    #now = datetime.datetime.now()
    #sensor_time = now.strftime("%H:%M:%S:%f")
    #value = adcSR.read(adc0)
    #print(value)
    #data_dict = {"sensor": sensor, "value": str(value), "time": sensor_time}
    #serialized_data = pickle.dumps(data_dict)
    value = adcSR.read(adc0)
    now = datetime.datetime.now()
    sensor_time = now.strftime("%H:%M:%S:%f")
    message = topic + ", " + sensor_time + ", " + str(value)

    print("Sending...")
    #s.send(serialized_data)
    s.send(message.encode())
    time.sleep(1)

s.close()

#This is the side that will run on the pi. It should send data (lets have it send random data once a second)

import socket
import sys
import time
import pickle
import random #for testing
sys.path.insert(1, '/home/pi/Documents/Code/PlantPlayground')
from DAQStreams import ADCStreamReader
from TrackingData import TrackingData
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

topic = "PP01/"
topic_sec = "PP01/SEC/"
topic_min = "PP01/MIN/"
sensor = "A0"
now = datetime.datetime.now()
sensor_time = now.strftime("%H:%M:%S:%f")
value = adcSR.read(adc0)
td = TrackingData()
last_60_values = []
for i in range(1, 60):
    last_60_values.append(0)

data_dict = {"time": sensor_time, "topic": topic, "sensor": sensor, "value": value}
serialized_data = pickle.dumps(data_dict)

while True:
    #todo set the above sensor, dict, serialized_data, etc here
    #value = random.randrange(-20, 20)
    for i in range(1, 60):
        time.sleep(1)
        now = datetime.datetime.now()
        sensor_time = now.strftime("%H:%M:%S:%f")
        value = adcSR.read(adc0)
        last_60_values[i-1] = value
        print(value)
        data_dict = {"time": sensor_time, "topic": topic_sec, "sensor": sensor, "value": value}
        serialized_data = pickle.dumps(data_dict)
        #print("Sending...")
        s.send(serialized_data)
        #self.update_data(self.td)
        data_dict = {"time": sensor_time, "topic": topic_min, "sensor": sensor, "value": td.stringify()}
        serialized_data = pickle.dumps(data_dict)
        print("Sending min..."+td.stringify())
        s.send(serialized_data)
s.close()

"""
    def update_data(self, td):
        td.counter = td.counter + 1
        if (td.c0_value > td.last_high):
            td.up_count = td.up_count + 1
            td.last_high = td.c0_value
        elif (td.last_low > td.c0_value):
            td.down_count = td.down_count + 1
            td.last_low = td.c0_value
        td.difference = td.up_count - td.down_count
        td.history.insert(td.c0_value, td.counter % 60)
        td.moving_average = self.update_moving_average(td)
            
    def update_moving_average(self, td):
        sum = 0
        if (td.counter < 60):
            mod60 = td.counter
        else:
            mod60 = 60
        for i in range (0, mod60):
            sum = sum + td.history[i % mod60]
        if (sum == 0):
            return 0
        return sum / mod60
        #print(td.stringify())
"""





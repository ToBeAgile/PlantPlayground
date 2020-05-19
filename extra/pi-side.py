#This is the side that will run on the pi. It should send data (lets have it send random data once a second)

import socket
import sys
import time
import json

#host = '192.168.1.5'
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

sensor = "CH0"
value = 13
sensor_time = 1039234.323

data_dict = {"sensor": sensor, "value": value, "time": sensor_time}
json_string = json.dumps(data_dict)

while True:
    #todo set the above sensor, dict, json_string, etc here
    print("Sending...")
    #s.send(b"Test")
    s.send(b'Hi')
    time.sleep(1)

s.close()

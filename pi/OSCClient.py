from pythonosc.udp_client import SimpleUDPClient

import sys
#sys.path.insert(1, '../')
#from services.ADCStreamReader import *

ip = "127.0.0.1"
port = 1337

client = SimpleUDPClient(ip, port)  # Create client

# Get data
mV = 1234

client.send_message("/PP01/ADC0/RAW/", mV)   # Send float message
# client.send_message("/some/address", [1, 2., "hello"])  # Send message with int, float and string
# sleep
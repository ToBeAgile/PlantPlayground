#Plant Playground

from ADS1115Reader import *
from StreamInfo import *
from CSVWriter import *
import datetime

GAIN = 16
DATA_RATE = 8
SLEEP = 1

#create an instance of ADS1115 Reader
reader = ADS1115Reader()
reader.open(channel=0, gain=16, data_rate=8, sleep=1) #open channel 0 stream

stream = StreamInfo(status="open", gain=GAIN, data_rate=DATA_RATE, sleep=SLEEP)

csvwriter = Writer(gain=GAIN)

#read from channel 0
#display on screen in a while loop
try:
    while True:
        value = reader.read(channel=0)
        now = datetime.datetime.now()
        print("Value = ", value)
        print (((now.strftime("%Y-%m-%d %H:%M:%S:%f")), (round((value*stream.voltsPerDivision*1000), 4)), (round((value*stream.voltsPerDivision*1000), 4))))
        csvwriter.write_voltage(name="Diff_V_1: ", value=value)
except KeyboardInterrupt:
    GPIO.cleanup()
    
  


#Plant Playground
import sys
import matplotlib
# insert at 1, 0 is the script path (or '' in REPL)
#sys.path.insert(1, '../services')
sys.path.insert(1, '/home/pi/Documents/Code/PlantPlayground')

from services.ADS1115Reader import *
from services.DataLogger import *
#from services.Plotter import *
#from ../services/ADS1115Reader import *
#from StreamInfo import *
#from CSVWriter import *
import datetime

GAIN = 16
DATA_RATE = 8
SLEEP = 1
CHANNEL = 0

#create an instance of ADS1115 Reader
reader = ADS1115Reader()
reader.open(channel=CHANNEL, gain=GAIN, data_rate=DATA_RATE, sleep=SLEEP) #open channel 0 stream

#instantiate the writer and write the header
dl= DataLogger()
dl.write("Plant bioelectric data log. Project: Setup")
dl.write(dl.filename)
dl.write("Gain: " + str(GAIN))
dl.write("Volts per division: " + str(reader.voltsPerDivision))
dl.write("Data rate: " + str(DATA_RATE))
dl.write("Sleep: " + str(SLEEP))
dl.write("Time                 Value in mV")

#instantiate the plotter
#my_plotter = Plotter()

#read from channel 0
#display on screen in a while loop
try:
    while True:
        value = reader.read()
        #my_plot(value)
        now = datetime.datetime.now()
        #print("Value = ", value)
        print((now.strftime("%H:%M:%S:%f"), (round((value), 4))))
        dl.write(((now.strftime("%H:%M:%S:%f")), (round((value), 4))))
        #csvwriter.write_voltage(name="Diff_V_1: ", value=value)
except KeyboardInterrupt:
        GPIO.cleanup()
            
      


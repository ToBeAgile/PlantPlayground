#Plant Playground
import sys
import matplotlib
# insert at 1, 0 is the script path (or '' in REPL)
#sys.path.insert(1, '../services')
sys.path.insert(1, '/home/pi/Documents/Code/PlantPlayground')

from pi.ADS1115Reader import *
from pi.DataLogger import *
#from services.Plotter import *
#from ../services/ADS1115Reader import *
#from StreamInfo import *
#from CSVWriter import *
import datetime

GAIN = 16
DATA_RATE = 64 # 8 # 8 16 32 64 128 250 475 860
SLEEP = 2
NUMBEROFCHANNELS = 2
DIFFERENTIAL1 = 0
DIFFERENTIAL2 = 3
# channel, status, gain, data_rate, sleep
# channel_dictionary = [(0:'closed', GAIN, DATA_RATE, SLEEP),(1:'closed', GAIN, DATA_RATE, SLEEP)]

CHANNEL0 = 0
CHANNEL1 = 1
CH0SLEEPTIME = 600
CH1SLEEPTIME = 600

#create an instance of ADS1115 Reader
reader = ADS1115Reader()

# channel 0 is the control (a potato) gets read a second every minute
reader.open(differential=0, gain=GAIN, data_rate=DATA_RATE, sleep=CH0SLEEPTIME) #open channel 0 stream
reader.open(differential=3, gain=GAIN, data_rate=DATA_RATE, sleep=CH1SLEEPTIME) #open channel 1 stream

#instantiate the writer and write the header
dl= DataLogger()
dl.write("Plant bioelectric data log. Project: Setup")
dl.write(dl.filename)
dl.write("Channel0 is connected to the plant using a tinned coppper wire.`")
dl.write("Channel1 is connected to the plant using a silver wire dipped in chlorix for 10 minutes.")
dl.write("The plant is in a grounded Faraday cage and the Raspbery Pi 4 is in a Faraday cage inside the Faraday cage with a common ground.")
dl.write("I throw out the first reading after I switch channels and readingns seem to be better (but not perfect).")
dl.write("Gain: " + str(GAIN))
dl.write("Volts per division: " + str(reader.voltsPerDivision))
dl.write("Data rate: " + str(DATA_RATE))
dl.write("Time                 Value in mV")

#instantiate the plotter
#my_plotter = Plotter()

#read from channel 0
#display on screen in a while loop
try:
    while True:
        # for each channel read(self, channel, gain, data_rate, sleep):
        c0_value = reader.read(DIFFERENTIAL1, GAIN, 860, 0) #Throw out first reading
        c0_value = reader.read(DIFFERENTIAL1, GAIN, DATA_RATE, CH0SLEEPTIME)
        c1_value = reader.read(DIFFERENTIAL2, GAIN, 860, 0) #Throw out first readinng
        c1_value = reader.read(DIFFERENTIAL2, GAIN, DATA_RATE, CH1SLEEPTIME)
         #my_plot(value)
        now = datetime.datetime.now()
        #print("Value = ", value)
        print((now.strftime("%H:%M:%S:%f"), (round((c0_value), 4)), (round((c1_value), 4))))
        dl.write(((now.strftime("%H:%M:%S:%f")), (round((c0_value), 4)), (round((c1_value), 4))))
        #csvwriter.write_voltage(name="Diff_V_1: ", value=value)
except KeyboardInterrupt:
        GPIO.cleanup()
            
      


#Plant Playground

from ADS1115Reader import *

#create an instance of ADS1115 Reader
adsobj = ADS1115Reader()

#read from channel 0
#display on screen in a while loop
try:
    while True:
        myval = adsobj.reader(0)
        print(myval)
except KeyboardInterrupt:
    GPIO.cleanup()

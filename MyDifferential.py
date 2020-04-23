# Simple demo of reading the difference between channel 1 and 0 on an ADS1x15 ADC.
# Author: Tony DiCola
# License: Public Domain

# Import the ADS1x15 module.
import Adafruit_ADS1x15
import array as arr
import time
import datetime
import csv

# Create an ADS1115 ADC (16-bit) instance.
adc = Adafruit_ADS1x15.ADS1115()

# Or create an ADS1015 ADC (12-bit) instance.
#adc = Adafruit_ADS1x15.ADS1015()

# Note you can change the I2C address from its default (0x48), and/or the I2C
# bus by passing in these optional parameters:
#adc = Adafruit_ADS1x15.ADS1015(address=0x49, busnum=1)

# Choose a gain of 1 for reading voltages from 0 to 4.09V.
# Or pick a different gain to change the range of voltages that are read:
#  - 2/3 = +/-6.144V
#  -   1 = +/-4.096V
#  -   2 = +/-2.048V
#  -   4 = +/-1.024V
#  -   8 = +/-0.512V
#  -  16 = +/-0.256V
# See table 3 in the ADS1015/ADS1115 datasheet for more info on gain.

# Build an array
# index, gainValue, voltage, voltsPerDivision
# 0, 0.66, 6.144, 0.00018750286106660564
# 1, 1, 4.096, 0.0001250019073777371
# 2, 2, 2.048, 6.250095368886855e-05
# 3, 4, 1.024, 3.125047684443427e-05
# 4, 8, 0.512, 1.5625238422217137e-05
# 5, 16, 0.256, 7.812619211108568e-06

GAIN = 16
index = 5
a = arr.array('f', [6.144, 4.096, 2.048, 1.024, 0.512, 0.256])
voltsPerDivision = (2 * a[index])/65535

writer=0

with open('./PlantProject/data_files/data.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Plant bioelectric data log. Project: Setup"])
    writer.writerow(["Gain: " + str(GAIN)])
    writer.writerow(["Volts per division: " + str(voltsPerDivision)])
    writer.writerow(["Time                       Raw  Value in mV"])

print('Press Ctrl-C to quit...')
counter = 0
volts = 0
value = 0
lastValue = 0
threashold = 2

while True:
    # Read the difference between channel 0 and 1 (i.e. channel 0 minus channel 1).
    # Note you can change the differential value to the following:
    #  - 0 = Channel 0 minus channel 1
    #  - 1 = Channel 0 minus channel 3
    #  - 2 = Channel 1 minus channel 3
    #  - 3 = Channel 2 minus channel 3
    value = adc.read_adc_difference(0, gain=GAIN, data_rate=8)
    # Note you can also pass an optional data_rate parameter above, see
    # simpletest.py and the read_adc function for more information.
    # Value will be a signed 12 or 16 bit integer value (depending on the ADC
    # precision, ADS1015 = 12-bit or ADS1115 = 16-bit).
    #print('Channel 0 minus 1: {0}'.format(value))
      # Pause for a second.
    time.sleep(60)
    if (value > lastValue + threashold) or   (value < lastValue - threashold):
        now = datetime.datetime.now()
        print (((now.strftime("%Y-%m-%d %H:%M:%S:%f")), (round((value*voltsPerDivision*1000), 4))))
        # print((value*voltsPerDivision*1000, value*voltsPerDivision*1000))
        with open('./PlantProject/data_files/data.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([now.strftime("%Y-%m-%d %H:%M:%S:%f"), value, value*voltsPerDivision*1000])
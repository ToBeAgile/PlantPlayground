#Class to write out data to a file
#takes the voltage data output by the ADS1115Reader Class
#writes out to the file only if the value changes by enough of a threshold
import csv
import datetime

class Writer:
    #open a file for writing here
    #todo ensure file close at destruction?
    threshold = 2
    
    #todo change index based on gain.
    def __init__(self, gain):
        self.gain = gain
        self.stream_info_dict = {0:6.144, 1:4.096, 2:2.048, 4:1.024, 8:0.512, 16:0.256}
        self.voltsPerDivision = (2 * self.stream_info_dict[self.gain])/65535
        with open('./data_files/data.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Plant bioelectric data log. Project: Setup"])
            writer.writerow(["Gain: " + str(self.gain)])
            writer.writerow(["Volts per division: " + str(self.voltsPerDivision)])
            writer.writerow(["Time                       Raw  Value in mV"])

    def write_voltage(self, name, value):
        #if the value has changed by the threshold, write it
        #todo add last_value tracking and threshold
        now = datetime.datetime.now()
        with open('./data_files/data.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([now.strftime("%Y-%m-%d %H:%M:%S:%f"), value, value*self.voltsPerDivision*1000])
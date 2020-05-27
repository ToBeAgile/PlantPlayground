from pythonosc.udp_client import SimpleUDPClient

import sys
import time
import timeit
import datetime
import threading

#sys.path.insert(1, '../')
sys.path.insert(1, '/home/pi/Documents/Code/PlantPlayground')
from pi.ADCStreamReader import *

class TrackingData:
    last_high = 0
    up_count = 0
    last_low = 0
    down_count = 0
    moving_average = 0
    difference = 0
    c0_value = 0
    moving_average = 0
    counter = 0
    history = [60]
    
    def __init__(self):
        dummy = 0
    
    def stringify(self):
        return("val: "+str(self.c0_value)+" avg: "+str(self.moving_average)+
               " hi: "+str(self.last_high)+" lo: "+str(self.last_low)+
               " dif: "+str(self.difference))


class OSCHandler():
    
    ip = "192.168.0.18" # internal ip address of MacBook Pro 
    port = 50000
    client = 0
    adcSR = 0
    adc0 = 0 
    adc3 = 0
    td = 0
    now = 0
    
    def __init__(self):
        self.client = SimpleUDPClient(self.ip, self.port)
        self.adcSR = ADCStreamReader()
        self.adc0 = self.adcSR.open(differential=0, gain=16, data_rate=8, sleep=0)
        #self.adc3 = self.adcSR.open(differential=3, gain=16, data_rate=8, sleep=0)
        self.td = TrackingData()
        self.now = datetime.datetime.now()

    def send_message(self, address, args):
        return self.client.send_message(address, args) 
        
    def OSCWriteRawContinuous(self):
        while True:
            try:
                time.sleep(0.05)
                td.c0_value = self.adcSR.read(self.adc0)
                self.send_message("/PP01/ADC0/RAW/", td.c0_value)
                #time.sleep(0.05)
                #c3_value = adcSR.read(adc3)
                #self.send_message("/PP01/ADC1/RAW/", c3_value)
            except KeyboardInterrupt:
                    GPIO.cleanup()



    
    def main_loop(self):
        try:
            while True:
                #self.td.initialize()          
                for x in range (1, 10):
                    time.sleep(0.1)
                    self.td.c0_value = self.adcSR.read(self.adc0)
                    self.broadcast_raw_format()
                    self.update_data(self.td)
                    #if (self.exceeds_tolerance(self.td)):
                #self.send_bundled_data(self.td)
                self.broadcast_sec_format(self.td)
            
        except KeyboardInterrupt:
                    GPIO.cleanup()

                
    def exceeds_tolerance(self, td):
        return (td.difference > 2 or -2 > td.difference) 
    
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
        mod60 = (td.counter % 60)+1
        for i in range (0, mod60):
            sum = sum + td.history[i % mod60]
        if (sum == 0):
            return 0
        return sum / mod60
        #print(td.stringify())
    
    def broadcast_raw_format(self):
        #time.sleep(0.1)
        self.c0_value = self.adcSR.read_without_sleep(self.adc0)
        self.send_message("/PP01/ADC0/RAW/", self.c0_value)

    def broadcast_sec_format(self, td):
        now = datetime.datetime.now()
        self.send_message("/PP01/ADC0/SEC/", now.strftime("%H:%M:%S:%f ")+self.td.stringify())   

    




"""   
===
     
                
                time.sleep(0.05)
                c3_value = adcSR.read(adc3)
                self.send_message("/PP01/ADC1/RAW/", c3_value)   # Send float message

                #c3_value = self.adc.read_adc_difference(self.d3, self.gain, self.data_rate)
                #self.client.send_message("/PP01/ADC1/RAW/", c3_value)   # Send float message
 
                now = datetime.datetime.now()
                #print("Value = ", value)
                print((now.strftime("%H:%M:%S:%f"), (round((c0_value), 4)), (round((c1_value), 4))))
                dl.write(((now.strftime("%H:%M:%S:%f")), (round((c0_value), 4)), (round((c1_value), 4))))
                #csvwriter.write_voltage(name="Diff_V_1: ", value=value)
                """

    







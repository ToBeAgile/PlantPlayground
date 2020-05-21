from pythonosc.udp_client import SimpleUDPClient

import sys
import time
import timeit

sys.path.insert(1, '/home/pi/Documents/Code/PlantPlayground/')
from pi.ADCStreamReader import *

class OSCWriter():
    
    ip = "192.168.0.18"
    port = 50000

    client = SimpleUDPClient(ip, port)  # Create client

    def send_message(self, address, args):
        return self.client.send_message(address, args) 
        
    def OSCWriteRawContinuous(self):
        adcSR = ADCStreamReader()
        adc0 = adcSR.open(differential=0, gain=16, data_rate=8, sleep=0)
        adc3 = adcSR.open(differential=3, gain=16, data_rate=8, sleep=0)
        
        while True:
            try:
                time.sleep(0.05)
                c0_value = adcSR.read(adc0)
                self.send_message("/PP01/ADC0/RAW/", c0_value)   # Send float message
                time.sleep(0.05)
                print("Hi")
                c3_value = adcSR.read(adc3)
                self.send_message("/PP01/ADC1/RAW/", c3_value)   # Send float message
            except KeyboardInterrupt:
                    GPIO.cleanup()
        
              
            """   
            
                for x in range (1,10)
                    last_high_c0 = 0
                    up_count_c0 = 0
                    last_low_c0 = 0
                    down_count_c0 = 0
                    # for each channel read(self, channel, gain, data_rate, sleep):
                    time.sleep(0.05)
                    c0_value = adcSR.read(adc0)
                    self.send_message("/PP01/ADC0/RAW/", c0_value)   # Send float message
                    if (c0_value > last_high_c0):
                        up_count_c0 =+ 1
                        last_high_c0 = c0_value
                    elif (last_low_c0 > c0_value):
                        down_count_c0 =+ 1
                        last_low_c0 = C0_value
                difference_c0 = up_count_c0 - down_count_c0
                if (difference_c0 > 2 || -2 > difference_c0)
                    log_value(c0_value)
                    
                
                def log_value(self, value)
     
                
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

    






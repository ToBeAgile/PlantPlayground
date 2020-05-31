import unittest
import threading
import sys
sys.path.insert(1, '/home/pi/Documents/Code/PlantPlayground/')
#sys.path.insert(1, '../')
from pi.ADCStreamReader import *
from pi.ADCStreamWrapper import *
from pi.OSCHandler import *
from pi.TrackingData import TrackingData

class OSCHandlerTest(unittest.TestCase):

    def test_exceeds_tolerance(self):
        td = TrackingData()
        h = OSCHandler()
        #assert h.exceeds_tolerance(td) == False
    
    def test_update_data(self):
        td = TrackingData()
        h = OSCHandler()
        h.update_data(td)
        #assert td.difference == 0
     
    def test_update_data_new_high(self):
        td = TrackingData()
        h = OSCHandler()
        td.value = 1
        h.update_data(td)
        #assert td.up_count == 1
        
    def test_update_data_new_low(self):
        td = TrackingData()
        h = OSCHandler()
        td.value = -1
        h.update_data(td)
        #assert td.down_count == 1

    def test_broadcast_raw_format(self):
        h = OSCHandler()
        h.broadcast_raw_format()
        
    def testOSCWriteRawContinuous(self):
        oscHandler = OSCHandler()
        #oscHandler.OSCWriteRawContinuous()       
        
    def test_main_loop(self):
        h = OSCHandler()
        td = TrackingData()
        h.main_loop()
        
    def test_broadcast_sec_format(self):
        h = OSCHandler()
        td = TrackingData()
        h.broadcast_sec_format(td)
        #t = threading.Timer(1, h.broadcast_sec_format())
        #t.start()
        #time.sleep(10)
        #h.main_loop()
        
"""    
        
        
  
    
    
    def testOSCWriteRawData(self):
        oscHandler = OSCHandler()
        adcSR = ADCStreamReader()
        adc = adcSR.open(differential=0, gain=16, data_rate=8, sleep=0)
        value = adcSR.read(adc)
        oscHandler.send_message("/PP01/ADC0/RAW/", value)
        print(value)

"""


if __name__ == '__main__':
    unittest.main()






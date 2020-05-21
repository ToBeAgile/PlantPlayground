import unittest
import sys
sys.path.insert(1, '/home/pi/Documents/Code/PlantPlayground/')
#sys.path.insert(1, '../')
from pi.ADCStreamReader import *
from pi.ADCStreamWrapper import *
from pi.OSCHandler import *

class OSCHandlerTest(unittest.TestCase):
    
    def testOSCWriteRawData(self):
        oscHandler = OSCHandler()
        adcSR = ADCStreamReader()
        adc = adcSR.open(differential=0, gain=16, data_rate=8, sleep=0)
        c0_value = adcSR.read(adc)
        oscHandler.send_message("/PP01/ADC0/RAW/", c0_value)
        print(c0_value)

    def testOSCWriteRawD0Negative(self):
        mock_adcSR = ADCStreamWrapper(-1) #use mock
        mock_adc = mock_adcSR.open(differential=0, gain=16, data_rate=8, sleep=0)
        mock_c0_value = mock_adcSR.read(mock_adc)
        assert mock_c0_value == -1
        
    def testOSCWriteRawD0Positive(self):
        mock_adcSR = ADCStreamWrapper(1) #use mock
        mock_adc = mock_adcSR.open(differential=0, gain=16, data_rate=8, sleep=0)
        mock_c0_value = mock_adcSR.read(mock_adc)
        assert mock_c0_value == 1
        
    def testOSCWriteRawcontinuous(self):
        oscHandler = OSCHandler()
        oscHandler.OSCWriteRawContinuous()
        

if __name__ == '__main__':
    unittest.main()






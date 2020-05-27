import unittest
import sys
sys.path.insert(1, '/home/pi/Documents/Code/PlantPlayground')

from pi.ADCStreamReader import *
from pi.ADS1115Reader import *


class SignalPlaygrountTest(unittest.TestCase):
    reader = ADCStreamReader()

    def test_ADCStreamReader_open(self):
        self.return_differential = self.reader.open(differential=0, gain=16, data_rate=8, sleep=0)
        assert self.reader.differential == self.return_differential
        assert self.reader.differential == 0
        assert self.reader.gain == 16
        assert self.reader.data_rate == 8
        assert self.reader.sleep == 0
        #value = self.reader.read(0, 16, 8, 0)
        
    def test_ADCStreamReader_read(self):
        self.return_differential = self.reader.open(differential=0, gain=16, data_rate=8, sleep=0)
        self.value = self.reader.read(self.reader.differential)
        #assert self.value != 0
        print (self.value)

    def test_ADCStreamReader_broadcastOSC(self):
        self.reader.broadcastOSC()
        #assert self.value != 0
        #print (self.value)
        

if __name__ == '__main__':
    unittest.main()
import unittest
import sys
sys.path.insert(1, '/home/pi/Documents/Code/PlantPlayground')

from pi.DAQStreams import *
from pi.ADS1115Reader import *


class ADCStreamReaderTest:
    reader = ADCStreamReader()
    
    def test_open(self, ADCStreamInfo):
        #create an ADCStreamInfo object, pass it to the factory method, and verify to object returned
        
        

class SignalPlaygroundTest(unittest.TestCase):
    reader = ADCStreamReader()

    def test_differential_stream(self):
        self.reader.open(reader_type='differential', channel=0, gain=16, data_rate=8, sleep=0)
        assert self.reader.reader_type == 'differential'
        assert self.reader.channel == 0
        assert self.reader.gain == 16
        assert self.reader.data_rate == 8
        assert self.reader.sleep == 0
        value = self.reader.read(0)
        print('Differential: ', value)
    
    def test_single_ended_stream(self):
        self.reader.open(reader_type='single_ended', channel=0, gain=16, data_rate=8, sleep=0)
        assert self.reader.reader_type == 'single_ended'
        value = self.reader.read(0)
        print('Single_ended: ', value)

    def test_differential_i2c(self):
        self.reader.open(reader_type='differential_i2c', channel=0, gain=16, data_rate=8, sleep=0)
        value = self.reader.read(0)
        print('i2c_diff: ', value)  

if __name__ == '__main__':
    unittest.main()
import unittest
import sys

sys.path.insert(1, '/home/pi/Documents/Code/PlantPlayground')
from pi.ADCStreamWrapper import *

ALWAYS_POSITIVE = 1
ALWAYS_NEGATIVE = -1
PASSTHRU = 0

class ADCStreamWrapperTest(unittest.TestCase):
    wrapper = 0
    
    def test_ADCWrapper_PassThru(self):
        wrapper = ADCStreamWrapper(PASSTHRU)
        real_value = wrapper.read(self.wrapper)
        #assert real_value == 0

    def test_ADCWrapper_Positive(self):
        wrapper = ADCStreamWrapper(ALWAYS_POSITIVE)
        real_value = wrapper.read(self.wrapper)
        assert real_value > 0

    def test_ADCWrapper_Negative(self):
        wrapper = ADCStreamWrapper(ALWAYS_NEGATIVE)
        real_value = wrapper.read(self.wrapper)
        assert 0 > real_value

if __name__ == '__main__':
    unittest.main()

        


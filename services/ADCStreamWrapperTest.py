import unittest
import sys

sys.path.insert(1, '../')
from ADCStreamWrapper import *

ALWAYS_POSITIVE = 1
ALWAYS_NEGATIVE = -1
PASSTHRU = 0

class ADCStreamWrapperTest(unittest.TestCase):
    
    def test_ADCWrapper_PassThru(self):
        wrapper = ADCStreamWrapper(PASSTHRU)
        #open, read, assert < 0
        dummy = 0

    def test_ADCWrapper_Positive(self):
        wrapper = ADCStreamWrapper(ALWAYS_POSITIVE)
        #open, read, assert < 0
        dummy = 0

    def test_ADCWrapper_Negative(self):
        wrapper = ADCStreamWrapper(ALWAYS_NEGATIVE)
        #open, read, assert < 0
        dummy = 0

        


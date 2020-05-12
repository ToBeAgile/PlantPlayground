import unittest
from PlantPlayground import *

class PlantPlaygrountTest(unittest.TestCase):
    reader = ADS1115Reader()
    def test_read_a_value(self):
        self.reader.open(channel=0, gain=16, data_rate=8, sleep=600)
        value = self.reader.read(channel=0)
        print("Value = ", value)
        assert False
        
        
if __name__ == __main__:
    unittest.main()


import unittest
import sys

sys.path.insert(1, '/home/pi/Documents/Code/PlantPlayground/')

from pi.StreamInfo import StreamInfo

class StreamInfoTest(unittest.TestCase):
    def test_retrieving_parameters_after_construction(self):
        si = StreamInfo('Open', gain=16, data_rate=8, sleep=0)
        self.assertEqual('Open', si.status)
        self.assertEqual(16, si.gain)
        self.assertEqual(8, si.data_rate)
        self.assertEqual(0, si.sleep)
        
if __name__ == '__main__':
    unittest.main()

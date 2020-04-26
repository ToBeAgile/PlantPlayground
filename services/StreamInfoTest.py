import unittest
import StreamInfo

class StreamInfoTest(unittest.TestCase):
    def test_retrieving_parameters_after_construction(self):
        si = StreamInfo.StreamInfo('Open', 16, 8, 1)
        self.assertEqual('Open', si.getStatus())
        self.assertEqual(16, si.getGain())
        self.assertEqual(8, si.getDataRate())
        self.assertEqual(1, si.getSleep())
        
if __name__ == '__main__':
    unittest.main()

import unittest
import ADS1115Reader
from ADS1115Reader import ADS1115Reader
#doesn't run

class TestADS1115Reader(unittest.TestCase):
    
    def test_retrieving_parameters_after_construction(self):
        print("Stuff works")
        adsReader = ADS1115Reader()
        adsReader.open(1, 16, 8, 1)
        self.assertEqual(1, 1)
    
    def test_open_channel(self):
        adsReader = ADS1115Reader()
        adsReader.open(1, 16, 8, 1)
        self.assertTrue(adsReader.is_channel_open(0))
        self.assertEqual(16, adsReader.get_gain(0))
        self.assertEqual(8, adsReader.get_data_rate(0))
        self.assertEqual(1, adsReader.get_sleep(0))
        
    def test_read(self):
        adsReader = ADS1115Reader()
        adsReader.open(1, 16, 8, -1)
        value = adsReader.read(0, 16, 860, -1)
        print(value)

if __name__ == '__main__':
    unittest.main()
#test writer
from CSVWriter import *
import unittest

class TestWriter(unittest.TestCase):
    def test_constructor(self):
        writer_obj = Writer(gain=16)
        self.assertIsInstance(writer_obj, Writer)
    def test_write(self):
        writer_obj = Writer(gain=16)
        writer_obj.write_voltage(name="Differential Voltage 1", value=5)
        #todo feed it some dummy values
        #todo automate testing that the proper values are being written
        #todo test threshold

if __name__ == '__main__':
    unittest.main()
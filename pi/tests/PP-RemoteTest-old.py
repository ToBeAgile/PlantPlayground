#! /user/bin/env python
#import text_wrap
import sys
import csv
import os
#sys.path.insert(1, '/home/pi/Documents/Code/PlantPlayground')
import unittest
import remote_utils


#from application.PlantPlayground import *

class PPRemoteTest(unittest.TestCase):
    def test_header(self):
        expected = """
            "Plant bioelectric data log by David Scott Bernstein. Project: Setup, File name: "
            "Software: PlantPlayground, File: PP-Remote.py, Version 0.1"
            """
        #self.assertEqual(text_wrap.deindent(expected)[1:], "/n".join(remote_utils.get_header_text()))
    def test_read_a_value(self):
        if os.path.isfile('hello.txt'):        
            os.remove('hello.txt')
        #self.assertTrue(remote_utils.big('hello.txt'))
        
        
if __name__ == '__main__':
    unittest.main()


import unittest
import os.path
from os import path
import datetime
import sys

sys.path.insert(1, '/home/pi/Documents/Code/PlantPlayground')
from services.DataLogger import *


class TestDataLogger(unittest.TestCase):
    
    def test_DataLogger_create_file(self):
        #arrange
        #delete the file if it exists
        now = datetime.datetime.now()
        project_name = "R0"
        test_filename = project_name + "-" + now.strftime("%Y-%m-%d") + ".csv"
        test_directory = "../tests/test_data/"
        test_path = test_directory + test_filename
        if(os.path.exists(test_path)):
            os.remove(test_path)
            
        #instantiate datalogger
        dl = DataLogger(test_directory)
        #dl = DataLogger()
        dl_filename = dl.filename
        dl_project_name = dl.project_name
        
        #act
        #test if it matches
        self.assertEqual(dl_filename, test_filename)
        #print(dl_filename)
        
        #check if it exists
        print(dl.full_path)
        print(dl.partial_path)
        self.assertTrue(path.exists(dl.full_path))
        dl.file.close()
        
        
    def test_DataLogger_append_file(self):
        #arrange
        #create the file
        now = datetime.datetime.now()
        project_name = "R0"
        test_filename = project_name + "-" + now.strftime("%Y-%m-%d") + ".csv"
        test_directory = "../tests/test_data/"
        test_path = test_directory + test_filename
        
        if(os.path.exists(test_path)):
            os.remove(test_path)
        
        file = open(test_path, "x")
        file.close()
            
        #instantiate datalogger
        dl = DataLogger(test_directory)
        #dl = DataLogger()
        dl_filename = dl.filename
        dl_project_name = dl.project_name
        
        #act
        #write to the file
        dl.file.write("hello")
        #ensure that filesize is nonzero
        dl.file.close()
        
        #assert
        #file size is greater than 0
        #os.stat('somefile.txt').st_size
        self.assertTrue((os.stat(dl.full_path).st_size) > 0)
        
    def test_DataLogger_write(self):
        #arrange
        #create the file
        test_directory = "../tests/test_data/"
        
        #instantiate datalogger
        dl = DataLogger(test_directory)
        original_size = os.stat(dl.full_path).st_size
        
        #act
        #write to the file
        dl.write("hello")
        dl.file.close()
        modified_size = os.stat(dl.full_path).st_size
        
        #assert
        #file size is greater than 0
        #os.stat('somefile.txt').st_size
        self.assertTrue(modified_size > original_size)
        

if __name__ == '__main__':
    unittest.main()
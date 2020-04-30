import datetime
import os.path
from os import path
import csv

class DataLogger:
    now = datetime.datetime.now()
    project_name = "R0"
    filename = project_name + "-" + now.strftime("%Y-%m-%d") + ".csv"
    full_path = "../data/" + filename
    def __init__(self, partial_path="../data/"):
        self.partial_path = partial_path
        self.full_path = self.partial_path + self.filename
        self.file = open(self.full_path, "a")
        self.file.close()
        
    def write(self, data):
        #self.file.write(data)
        with open(self.full_path, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([data])
    
    
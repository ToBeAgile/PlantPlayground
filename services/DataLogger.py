import datetime
import os.path
from os import path

class DataLogger:
    now = datetime.datetime.now()
    project_name = "R0"
    filename = project_name + "-" + now.strftime("%Y-%m-%d") + ".csv"
    full_path = "../data/" + filename
    def __init__(self, partial_path="../data/"):
        self.partial_path = partial_path
        self.full_path = self.partial_path + self.filename
        self.file = open(self.full_path, "w")
        
    def write(self, data):
        self.file.write(data)
    
    
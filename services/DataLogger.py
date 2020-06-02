import datetime
import os.path
from os import path
import csv
import sys
sys.path.insert(1, '/Users/davidscottbernstein/Dropbox/Dev/Python/Projects/PlantPlayground')


class DataLogger:
    now = datetime.datetime.now()
    project_name = "R0"
    filename = project_name + "-" + now.strftime("%Y-%m-%d") + ".csv"
    full_path = "../data/" + filename
    def __init__(self, partial_path="../data/"):
        self.partial_path = partial_path
        self.full_path = self.partial_path + self.filename
        #if exists append, otherwise create
        if os.path.isfile(self.full_path):
            with open(self.full_path, 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Plant bioelectric data log. Project: Setup"])
                writer.writerow(["Time", "Value"])
                # writer.writerow(["Time"])
            file.close()
        else:
            with open(self.full_path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Plant bioelectric data log. Project: Setup"])
                writer.writerow(["Time", "Value"])
                # writer.writerow(["Time"])
            file.close()

    def write(self, time, value):
        #self.file.write(data)
        with open(self.full_path, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([time, value])
    
    
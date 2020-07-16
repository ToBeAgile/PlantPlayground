import os.path
import csv
from typing import List

def a(self):
    return True

def big(full_path: str, file_name:str = '', sensor_read_time:int = 1, a_gain:int = 1, a_data_rate:int = 1, a_mv_per_division:int = 1,b_mv_per_division:int = 1,
        b_gain:int = 1, b_data_rate:int = 1):
    if os.path.isfile(full_path):
        #with open(full_path, 'a', newline='', buffering=1) as file:
            #writer = csv.writer(file)
        file = open(full_path, 'a', newline='', buffering=1)
        writer = csv.writer(file)
    else:
        #with open(full_path, 'w', newline='', buffering=1) as file:
        file = open(full_path, 'w', newline='', buffering=1)            
        writer = csv.writer(file)
        #writer and write the header
        for r in get_header_text():
            writer.writerow([r])
        writer.writerow(["Reading 2 differential channels in milivolts with a sensor read frequency of " + str(sensor_read_time) + "."])
        writer.writerow(["The plant is in a Faraday cage and the Pi 4 is in a Faraday cage inside the Faraday cage with a common ground."])
        writer.writerow(["Channel A is connected to a potato in a Faraday cage. Channel B is connected to a plant in a Faraday cage."])
        writer.writerow(["Gain: " + str(a_gain) + ", Data Rate: " + str(a_data_rate) + ", Volts per Division: " + str(a_mv_per_division) + "."])
        writer.writerow(["Channels A and B are connected using a silver-silver chloride wire that I made myself."])
        writer.writerow(["Gain: " + str(b_gain) + ", Data Rate: " + str(b_data_rate) + ", Volts per Division: " + str(b_mv_per_division) + "."])
    file.close()
        
    return False
def get_header_text(file_name:str = '', sensor_read_time:int = 1, a_gain:int = 1, a_data_rate:int = 1, a_mv_per_division:int = 1,b_mv_per_division:int = 1,
        b_gain:int = 1, b_data_rate:int = 1) -> List[str]:
    return [f"Plant bioelectric data log by David Scott Bernstein. Project: Setup, File name: {file_name}",
                 "Software: PlantPlayground, File: PP-Remote.py, Version 0.1"]

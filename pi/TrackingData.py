import datetime


class TrackingData:
    now = 0
    topic = ""
    sensor = ""
    
    last_high = 0
    up_count = 0
    last_low = 0
    down_count = 0
    difference = 0
    value = 0
    moving_average = 0
    counter = 0
    history = [60]
    
    def __init__(self):
        dummy = 0
    
    def stringify(self):
        self.now = datetime.datetime.now()
        return(str(self.now) + self.topic + self.sensor + " val: " + str(self.value)
               + " avg: " + str(self.moving_average) + " dif: " + str(self.difference))

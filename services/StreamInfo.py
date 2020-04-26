import unittest

class StreamInfo:
    def __init__(self, status, gain, data_rate, sleep):
        self.status = status
        self.gain = gain
        self.data_rate = data_rate
        self.sleep = sleep
        
    def getStatus(self):
        return self.status
    
    def getGain(self):
        return self.gain
    
    def getDataRate(self):
        return self.data_rate
    
    def getSleep(self):
        return self.sleep
        

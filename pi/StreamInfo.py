import unittest

class StreamInfo:
    #gain = 8
    def __init__(self, status, gain, data_rate, sleep):
        self.status = status
        self.gain = gain
        self.data_rate = data_rate
        self.sleep = sleep
        self.stream_info_dict = {0:6.144, 1:4.096, 2:2.048, 4:1.024, 8:0.512, 16:0.256}
        self.voltsPerDivision = (2 * self.stream_info_dict[self.gain])/65535
        
    #index = 5
    #a = arr.array('f', [6.144, 4.096, 2.048, 1.024, 0.512, 0.256])
    #[(0, 6.144), (1, 4.096), (2, 2.048), (4, 1.024), (8, 0.512), (16, 0.256)]
    

        

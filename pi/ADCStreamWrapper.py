import sys
import timeit

#sys.path.insert(1, '../')
sys.path.insert(1, '/home/pi/Documents/Code/PlantPlayground')
from pi.ADCStreamReader import ADCStreamReader

WRAPPER_PASSTHRU = 0
WRAPPER_POSITIVE = 1
WRAPPER_NEGATIVE = -1

class ADCStreamWrapper:

    adcSR = 0    
    def __init__(self, wrapper_type):
        self.wrapper_type = wrapper_type
        self.adcSR = ADCStreamReader()
        
    def open(self, differential, gain, data_rate, sleep):
        
        return self.adcSR.open(differential, gain, data_rate, sleep)
    
    def read(self, differential):
        
        if (self.wrapper_type == WRAPPER_PASSTHRU):
            
            return self.adcSR.read(differential)
        
        elif (self.wrapper_type == WRAPPER_POSITIVE):
            
            return WRAPPER_POSITIVE
        
        elif (self.wrapper_type == WRAPPER_NEGATIVE):
            
            return WRAPPER_NEGATIVE
            
 

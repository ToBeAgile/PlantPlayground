import sys
import timeit

sys.path.insert(1, '../')


class ADCStreamWrapper:
    adcSR = adcStreamReader()
    
    def __init__(self, wrapper_type):
        self.wrapper_type = wrapper_type
        

    
    

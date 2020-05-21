#ADCThread - main thread to monitor 2 channels of input from ADS1115
import time

"""
In a forever loop:
    Wait 5 ms
    Read a value from differential 0
    Update value 0
    Write value 0 to the network
    Wait 5 ms
    Read a value from differential 1
    Update value 1
    Write value 1 to the network


"""
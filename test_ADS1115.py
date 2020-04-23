#test ADS1115Reader
from ADS1115Reader import *

adsobj = ADS1115Reader()

myval = adsobj.reader(0)
print(myval)
import sys
import unittest
from approvaltests.approvals import verify

sys.path.insert(1, '/home/pi/Documents/Code/PlantPlayground')
#import pi.PPRemote.py
class User():
    pass

class GettingStartedTest(unittest.TestCase):

    def test_simple(self):
        result = "Hello ApprovalTests"
        verify(str(result))
        
    #def test_simple2(self):
        #user = User()
        #verify(str(user))
    

if __name__ == "__main__":
    unittest.main()
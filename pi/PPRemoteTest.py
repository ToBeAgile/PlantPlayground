import sys
import unittest
from approvaltests.approvals import verify

sys.path.insert(1, '/home/pi/Documents/Code/PlantPlayground')
#import pi.PPRemote.py

class GettingStartedTest(unittest.TestCase):
    def test_simple(self):
        verify("Hello ApprovalTests")


if __name__ == "__main__":
    unittest.main()
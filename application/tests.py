import unittest

def suite():
    suite = unittest.TestSuite()
    #suite.addTest()
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
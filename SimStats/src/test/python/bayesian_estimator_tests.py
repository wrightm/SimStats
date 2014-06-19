'''
Created on 20 Jun 2014

@author: wrightm
'''
import unittest

class LikelihoodTest(unittest.TestCase):


    def testName(self):
        pass
    
class BayesianEstimatorTest(unittest.TestCase):


    def testName(self):
        pass


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    suite = unittest.TestSuite()
    suite.addTests([LikelihoodTest,BayesianEstimatorTest])
    unittest.TextTestRunner(verbosity=2).run(suite)
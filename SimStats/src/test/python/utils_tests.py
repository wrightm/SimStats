'''
Created on 18 Jun 2014

@author: wrightm
'''
import unittest
from src.main.python.utils import test_obj_subclass, test_obj_instance


class UtilsTest(unittest.TestCase):


    def test_test_obj_subclass(self):
        self.assertRaises(TypeError, test_obj_subclass, [], dict)
    
    def test_test_obj_instance(self):
        self.assertRaises(TypeError, test_obj_instance, [], dict)
    

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    suite = unittest.TestSuite()
    suite.addTests([UtilsTest])
    unittest.TextTestRunner(verbosity=2).run(suite)
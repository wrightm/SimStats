'''
Created on 13 Jun 2014

@author: wrightm
'''
import unittest
from src.main.python.discrete_distributions import DictWrapper


class DictWrapperTest(unittest.TestCase):


    def setUp(self):
        d = {0:0.0,1:1.0,2:2.0,3:4.0}
        self.dct_wrapper = DictWrapper(d, name='test_wrapper')
    
    def tearDown(self):
        pass
    
    def test_delete_magic_method(self):
        del self.dct_wrapper[0]
        self.assertEqual(self.dct_wrapper.get(0), None)

    def test_getitem_magic_method(self):
        self.assertEqual(self.dct_wrapper[1], 1.0)
    
    def test_contains_magic_method(self):
        outcome = False
        if 1 in self.dct_wrapper:
            outcome = True
        self.assertEqual(outcome, True)
     
    def test_len_magic_method(self):
        self.assertEqual(len(self.dct_wrapper),4)
        
    def test_iter_magic_method(self):
        d = {}
        for k, y in self.dct_wrapper:
            d[k] = y 
        self.assertEqual(self.dct_wrapper, d)
        
    def test_str_magic_method(self):
        self.assertEqual(str(self.dct_wrapper), "{0: 0.0, 1: 1.0, 2: 2.0, 3: 4.0}")

    
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
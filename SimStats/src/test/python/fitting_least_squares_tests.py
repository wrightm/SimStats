'''
Created on 17 Jun 2014

@author: wrightm
'''
import unittest
from src.main.python.fitting_least_squares import LeastSquares
from src.main.python.discrete_distributions import Pmf


class LeastSquaresTest(unittest.TestCase):

    def setUp(self):
        
        self.xs = [4,4]
        self.ys = [4,4]
        
        self.least_squares = LeastSquares(self.xs, self.ys)
        
    def tearDown(self):
        pass

    def test_fit_line(self):
        self.assertEqual(self.least_squares.fit_line(), (self.xs, self.ys))
    
    def test_fit_line_pmf(self):
        pmf = Pmf(dict(zip(self.xs, self.ys)))
        self.assertEqual(self.least_squares.fit_line_pmf(), pmf)
    
    def test_gradient(self):
        self.assertEqual(self.least_squares.gradient(), 0)
    
    def test_intercept(self):
        self.assertEqual(self.least_squares.intercept(), 4)
    
    def test_residuals(self):
        self.assertEqual(self.least_squares.residuals(), [0,0])
    
    def test_coefficient_of_determination(self):
        self.assertEqual(self.least_squares.coefficient_of_determination(), 1)
    
    

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test']
    suite = unittest.TestSuite()
    suite.addTests([LeastSquaresTest])
    unittest.TextTestRunner(verbosity=2).run(suite)
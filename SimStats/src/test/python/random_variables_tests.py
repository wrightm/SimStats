'''
Created on 19 Jun 2014

@author: wrightm
'''
import unittest
from src.main.python.random_variables import Exponential, Erlang, Gumbel, Normal,\
    LogNormal, Pareto, Sum, Uniform, generate_sample


class RandomVariableTest(unittest.TestCase):


    def test_exponential(self):
        expo_rnd = Exponential(0.5).generate()
        self.assertGreaterEqual(expo_rnd, 0.0)
        
    def test_erlang(self):
        erlang_rnd = Erlang(0.5,1)
        self.assertGreaterEqual(erlang_rnd, 0.0)
        
    def test_gumbel(self):
        gumbel_rnd = Gumbel(0.5, 1)
        self.assertGreaterEqual(gumbel_rnd, 0.0)

    def test_normal(self):
        normal_rnd = Normal(0.5, 1)
        self.assertGreaterEqual(normal_rnd, 0.0)
        
    def test_lognormal(self):
        lognormal_rnd = LogNormal(0.5,1)
        self.assertGreaterEqual(lognormal_rnd, 0.0)
        
    def test_pareto(self):
        pareto_rnd = Pareto(0.5, 1)
        self.assertGreaterEqual(pareto_rnd, 0.0)
        
    def test_sum(self):
        sum_rnd = Sum(Normal(0.5,1),Pareto(0.5,1))
        self.assertGreaterEqual(sum_rnd, 0.0)
        
    def test_uniform(self):
        uniform_rnd = Uniform(0,100,100)
        self.assertGreaterEqual(uniform_rnd, 0.0)
    
    def test_generate_sample(self):
        gen_sample = generate_sample(Normal(0.5,1), 10)
        self.assertEqual(len(gen_sample), 10)
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    suite = unittest.TestSuite()
    suite.addTests([RandomVariableTest])
    unittest.TextTestRunner(verbosity=2).run(suite)
'''
Created on 20 Jun 2014

@author: wrightm
'''
import unittest
from src.main.python.bayesian_estimator import Likelihood, ExponentialLikelihood,\
    ConditionalExponetialLikelihood, LikelihoodOfSeeingASetOfNumberUpperBound,\
    LikelihoodOfSeeingASetOfNumberLowerBound, BayesianEstimator
from src.main.python.discrete_distributions import make_pmf_from_list

class LikelihoodTest(unittest.TestCase):


    def test_likelihood(self):
        likeli = Likelihood()
        self.assertRaises(NotImplementedError, likeli.get_likelihood, '', '')
    
    def test_exponetial_likelihood(self):
        likeli = ExponentialLikelihood()
        self.assertEquals(likeli.get_likelihood([0,0,0], 1), 1)
    
    def test_conditional_exponetial_likelihood(self):
        likeli = ConditionalExponetialLikelihood(0.0,0.0)
        self.assertEquals(likeli.get_likelihood([0,0,0], 1), 1)
    
    def test_likelihood_of_seeing_a_set_0f_number_upper_bound(self):
        likeli = LikelihoodOfSeeingASetOfNumberUpperBound()
        self.assertEquals(likeli.get_likelihood([2,2,2], 1), 0.0)
    
    def test_likelihood_of_seeing_a_set_0f_number_lower_bound(self):
        likeli = LikelihoodOfSeeingASetOfNumberLowerBound()
        self.assertEquals(likeli.get_likelihood([0,0,0], 1), 0.0)
  
class TestLikelihood(Likelihood):
    
    def get_likelihood(self, evidence, hypothesis):
        param = hypothesis
        likelihood = 1
        for x in evidence:
            likelihood *= param * x
        return likelihood
        
class BayesianEstimatorTest(unittest.TestCase):

    def setUp(self):
        pmf = make_pmf_from_list([1,1,1,1])
        self.bayesian_est = BayesianEstimator(pmf, [1,1,1,1],TestLikelihood())

    def test_get_posterior(self):
        pmf = make_pmf_from_list([1,1,1,1])
        self.assertEqual(self.bayesian_est.get_posterior(), pmf)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    suite = unittest.TestSuite()
    suite.addTests([LikelihoodTest,BayesianEstimatorTest])
    unittest.TextTestRunner(verbosity=2).run(suite)
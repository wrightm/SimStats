'''
Created on 30 Jun 2014

@author: wrightm
'''
import unittest
from src.main.python.hypothesis_test import BayesianResult, BayesianResultSuite,\
    HypoTestResult, HypoResultSuite, HypothesisTest,\
    HypothesisTestDifferenceInMean


class BayesianResultTest(unittest.TestCase):

    def setUp(self):
        self.bayesian_result = BayesianResult(1.0,1.0,1.0,1.0)
    
    def test_get_prior(self):
        self.assertEqual(self.bayesian_result.get_prior(), 1.0)

    def test_get_posterior(self):
        self.assertEqual(self.bayesian_result.get_posterior(), 1.0)
    
    def test_get_likelihood(self):
        self.assertEqual(self.bayesian_result.get_likelihood(), 1.0)
    
    def test_get_normalisation(self):
        self.assertEqual(self.bayesian_result.get_normalisation(), 1.0)
        
class BayesianResultSuiteTest(unittest.TestCase):
    
    def setUp(self):
        self.bayesian_result_suite = BayesianResultSuite(BayesianResult(1.0,1.0,1.0,1.0),BayesianResult(1.0,1.0,1.0,1.0),BayesianResult(1.0,1.0,1.0,1.0))
    
    def test_get_median_bayesian_result(self):
        self.assertEqual(self.bayesian_result_suite.get_median_bayesian_result().get_prior(),1.0)
        
    def test_get_plus_sigma_bayesian_result(self):
        self.assertEqual(self.bayesian_result_suite.get_plus_sigma_bayesian_result().get_prior(),1.0)
    
    def test_get_minus_sigma_bayesian_result(self):
        self.assertEqual(self.bayesian_result_suite.get_minus_sigma_bayesian_result().get_prior(),1.0)
    
    def test_type_error(self):
        self.assertRaises(TypeError, BayesianResultSuite, 1.0,1.0,1.0)
    
class HypoTestResultTest(unittest.TestCase):
    
    def setUp(self):
        
        d = {'median_pvalue':1.0,
             'median_right_tail':1.0,
             'median_left_tail':1.0,
             'plus_one_sigma_pvalue':1.0,
             'plus_one_sigma_right_tail':1.0,
             'plus_one_sigma_left_tail':1.0,
             'minus_one_sigma_pvalue':1.0,
             'minus_one_sigma_right_tail':1.0,
             'minus_one_sigma_left_tail':1.0 }
        
        self.hypo_test_result = HypoTestResult(d)
        
    def test_get_median_pvalue(self):
        self.assertEqual(self.hypo_test_result.get_median_pvalue(), 1.0)
        
    def test_get_median_right_tail(self):
        self.assertEqual(self.hypo_test_result.get_median_right_tail(), 1.0)
        
    def test_get_median_left_tail(self):
        self.assertEqual(self.hypo_test_result.get_median_left_tail(), 1.0)
        
    def test_get_plus_one_sigma_pvalue(self):
        self.assertEqual(self.hypo_test_result.get_plus_one_sigma_pvalue(), 1.0)
        
    def test_get_plus_one_sigma_right_tail(self):
        self.assertEqual(self.hypo_test_result.get_plus_one_sigma_right_tail(), 1.0)
        
    def test_get_plus_one_sigma_left_tail(self):
        self.assertEqual(self.hypo_test_result.get_plus_one_sigma_left_tail(), 1.0)
        
    def test_get_minus_one_sigma_pvalue(self):
        self.assertEqual(self.hypo_test_result.get_minus_one_sigma_pvalue(), 1.0)
        
    def test_get_minus_one_sigma_right_tail(self):
        self.assertEqual(self.hypo_test_result.get_minus_one_sigma_right_tail(), 1.0)
        
    def test_get_minus_one_sigma_left_tail(self):
        self.assertEqual(self.hypo_test_result.get_minus_one_sigma_left_tail(), 1.0)
        
    def test_type_error(self):
        self.assertRaises(TypeError, HypoTestResult, 1.0)
        
class HypoResultSuiteTest(unittest.TestCase):
    
    def setUp(self):
         
        d = {'median_pvalue':1.0,
             'median_right_tail':1.0,
             'median_left_tail':1.0,
             'plus_one_sigma_pvalue':1.0,
             'plus_one_sigma_right_tail':1.0,
             'plus_one_sigma_left_tail':1.0,
             'minus_one_sigma_pvalue':1.0,
             'minus_one_sigma_right_tail':1.0,
             'minus_one_sigma_left_tail':1.0 }

        self.hypo_result_suite = HypoResultSuite(HypoTestResult(d),
                                                 HypoTestResult(d),
                                                 BayesianResultSuite(BayesianResult(1.0,1.0,1.0,1.0),BayesianResult(1.0,1.0,1.0,1.0),BayesianResult(1.0,1.0,1.0,1.0)))
                                                    
    def test_get_null_hypo_results(self):
        self.assertEqual(self.hypo_result_suite.get_null_hypo_results().get_median_pvalue(), 1.0)
        
    def test_get_alternative_hypo_result(self):
        self.assertEqual(self.hypo_result_suite.get_alternative_hypo_result().get_median_pvalue(), 1.0)
        
    def test_get_bayesian_result_suite(self):
        self.assertEqual(self.hypo_result_suite.get_bayesian_result_suite().get_median_bayesian_result().get_prior(), 1.0)
        
    def test_type_error(self):
        self.assertRaises(TypeError, HypoResultSuite, 1.0,1.0,1.0)
        
class HypothesisTestTests(unittest.TestCase):
    
    def setUp(self):
        pmf = [1.0,1.0,1.0,1.0,1.0,1.0]
        options = {'partition':True,
                   'trials':10}
        self.hypo_test = HypothesisTest(pmf, pmf, pmf, options)
        
    def test_test(self):
        self.assertRaises(NotImplementedError, self.hypo_test.test,'', '', '', '')
        
    def test_validate_objects(self):
        self.assertRaises(TypeError, HypoResultSuite, 1.0, 1.0, 1.0, 1.0)
        
    def test_run_test(self):
        self.assertRaises(NotImplementedError, self.hypo_test.run_test)
        
class HypothesisTestDifferenceInMeanTest(unittest.TestCase):

    def setUp(self):
        self.pmf = [1.0,1.0,1.0,1.0,1.0,1.0]
        options = {'partition':True,
                   'trials':10}
        self.hypo_test = HypothesisTestDifferenceInMean(self.pmf, self.pmf, self.pmf, options)
        
    def test_run_test(self):
        result = self.hypo_test.run_test()
        self.assertEqual(result.get_null_hypo_results().get_median_pvalue(),2.0)
        self.assertEqual(result.get_alternative_hypo_result().get_median_pvalue(),2.0)
        self.assertEqual(result.get_bayesian_result_suite().get_median_bayesian_result().get_posterior(),1.0)
        
        
    def test_test(self):
        result = self.hypo_test.test([1.0,1.0,1.0,1.0,1.0,1.0], [1.0,1.0,1.0,1.0,1.0,1.0], [1.0,1.0,1.0,1.0,1.0,1.0], [1.0,1.0,1.0,1.0,1.0,1.0])
        self.assertEqual(result.get_median_pvalue(), 2.0)
        self.assertEqual(result.get_median_left_tail(), 1.0)
        self.assertEqual(result.get_median_right_tail(), 1.0)
        self.assertEqual(result.get_plus_one_sigma_pvalue(), 2.0)
        self.assertEqual(result.get_plus_one_sigma_left_tail(), 1.0)
        self.assertEqual(result.get_plus_one_sigma_right_tail(), 1.0)
        self.assertEqual(result.get_minus_one_sigma_pvalue(), 2.0)
        self.assertEqual(result.get_minus_one_sigma_left_tail(), 1.0)
        self.assertEqual(result.get_minus_one_sigma_right_tail(), 1.0)
        
    def test_pvalue(self):
        self.assertEqual(self.hypo_test.pvalue([1.0,1.0,1.0,1.0,1.0,1.0], [1.0,1.0,1.0,1.0,1.0,1.0], 0.0), (2.0,1.0,1.0))
    
    def test_resample(self):
        self.assertEqual(self.hypo_test._resample([1.0], [1.0]), 0.0)
    
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    suite = unittest.TestSuite()
    suite.addTest([BayesianResultTest,
                   BayesianResultSuiteTest,
                   HypoTestResultTest,
                   HypoResultSuiteTest,
                   HypothesisTestTests,
                   HypothesisTestDifferenceInMeanTest])
    unittest.TextTestResult(verbosity=2).run(suite)
import unittest
from src.main.python.chi_squared_test import PmfProbabilities,\
    PmfProbabilityRange, ChiSquaredTest
from src.main.python.discrete_distributions import make_pmf_from_list
import copy


class PmfProbabilitiesTests(unittest.TestCase):
    
    def test_pmf_probabilities(self):
        pmf_probabilities = PmfProbabilities()
        self.assertRaises(NotImplementedError, pmf_probabilities.get_probabilities, 'test')
        
    def test_pmf_probability_range_exception(self):
        pmf_prob = PmfProbabilityRange(0,10)
        self.assertRaises(TypeError, pmf_prob.get_probabilities, [])
    
    def test_pmf_probability_range_get_probabilities(self):
        lst = [0,0,0,0,1,1,1,1,2,2,2,2,3,3,3,3]
        pmf = make_pmf_from_list(lst)
        pmf_probabilities = PmfProbabilityRange(0, 3)
        self.assertEqual(pmf_probabilities.get_probabilities(pmf), 0.75)
    
    
class ChiSquaredTestTests(unittest.TestCase):
    
    def setUp(self):
        lst = [0,0,0,0,1,1,1,1,2,2,2,2,3,3,3,3]
        observed = make_pmf_from_list(lst)
        expected = copy.deepcopy(observed)
        pmf_probabilities = PmfProbabilityRange(0, 3)
        self.chi_squared_test = ChiSquaredTest(observed, expected, [pmf_probabilities.get_probabilities], ntrials=10)
        
    def test_get_expected_probabilities(self):
        self.assertEqual(self.chi_squared_test.get_expected_probabilities(), [[0.75]])
        
    def test_get_observed_probabilities(self):
        self.assertEqual(self.chi_squared_test.get_observed_probabilities(), [[0.75]])
        
    def test_get_threshold_chi2(self):
        self.assertEqual(self.chi_squared_test.get_threshold_chi2(), 0.0)
        
    def test_get_simulated_chi2s(self):
        self.assertEqual(len(self.chi_squared_test.get_simulated_chi2s()), 10)
        
    def test_get_pvalue(self):
        self.assertEqual(self.chi_squared_test.get_pvalue(),1.0)
        
if __name__ == '__main__':
    pass
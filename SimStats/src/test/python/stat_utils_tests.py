'''
Created on 18 Jun 2014

@author: wrightm
'''
import unittest
from src.main.python.discrete_distributions import make_hist_from_list,\
    make_pmf_from_list, make_cdf_from_list
from src.main.python.stat_utils import mean, variance, standard_dev, zscores,\
    zscore, zscores_correlation, covariance, correlation, serial_correlation,\
    ranks, spearman_correlation, differences_adj_elements


class StatUtilTest(unittest.TestCase):


    def test_mean_histogram(self):
        
        lst = [4,4,4,4,4]
        hist = make_hist_from_list(lst)
        self.assertEqual(mean(hist), 4)
    
    def test_mean_pmf(self):
        
        lst = [4,4,4,4,4]
        pmf = make_pmf_from_list(lst)
        self.assertEqual(mean(pmf), 4)
    
    
    def test_mean_cdf(self):

        lst = [4,4,4,4,4]
        cdf = make_cdf_from_list(lst)
        self.assertEqual(mean(cdf), 4)      
        
    
    def test_mean_lst(self):
        
        lst = [4,4,4,4,4]
        self.assertEqual(mean(lst), 4)
    
    def test_mean_raise(self):
        
        self.assertRaises(TypeError, mean, 4)
    
    def test_variance_histogram(self):
        
        lst = [4,4,4,4,4]
        hist = make_hist_from_list(lst)
        self.assertEqual(variance(hist), 0)
    
    def test_variance_pmf(self):

        lst = [4,4,4,4,4]
        pmf = make_pmf_from_list(lst)
        self.assertEqual(variance(pmf), 0)
    
    def test_variance_cdf(self):
        
        lst = [4,4,4,4,4]
        cdf = make_cdf_from_list(lst)
        self.assertEqual(variance(cdf), 0)
    
    def test_variance_lst(self):
        
        lst = [4,4,4,4,4]
        self.assertEqual(variance(lst), 0)
    
    def test_variance_raise(self):
        
        self.assertRaises(TypeError, variance, 0)

    def test_standard_dev(self):
        
        lst = [4,4,4,4,4]
        self.assertEqual(standard_dev(lst), 0)
    
    def test_zscores_histogram(self):
        
        lst = [4,4,4,4,4]
        hist = make_hist_from_list(lst)
        self.assertEqual(zscores(hist), [0])
    
    def test_zscores_pmf(self):
        
        lst = [4,4,4,4,4]
        pmf = make_pmf_from_list(lst)
        self.assertEqual(zscores(pmf), [0])
    
    def test_zscores_cdf(self):
        
        lst = [4,4,4,4,4]
        cdf = make_cdf_from_list(lst)
        self.assertEqual(zscores(cdf), [0])
    
    def test_zscores_lst(self):
        
        lst = [4,4,4,4,4]
        self.assertEqual(zscores(lst), [0,0,0,0,0])
    
    def test_zscores_raise(self):
        
        self.assertRaises(TypeError, zscores, 0)
    
    def test_zscore(self):
        
        self.assertEqual(zscore(2, 1, 1), 1)
    
    def test_zscores_correlation(self):
        
        lst = [4,4,4,4,4]
        self.assertEqual(zscores_correlation(lst, lst), 0)
    
    def test_covariance(self):
        
        lst = [4,4,4,4,4]
        self.assertEqual(covariance(lst, lst), 0)
    
    
    def test_correlation(self):
        
        lst = [4,4,4,4,4]
        self.assertEqual(correlation(lst, lst), 0)
    
    def test_serial_correlation(self):
        
        lst = [4,4,4,4,4]
        self.assertEqual(serial_correlation(lst), 0)
    
    def test_spearman_correlation(self):
        
        lst = [4,4,4,4,4]
        self.assertAlmostEqual(spearman_correlation(lst,lst), 1, 1)
    
    def test_ranks(self):
        
        lst = [4,4,4,4,4]
        self.assertEqual(ranks(lst), [1,2,3,4,5])
    
    def test_differences_adj_elements(self):
        
        lst = [4,4,4,4,4]
        self.assertEqual(differences_adj_elements(lst), [0,0,0,0])

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    suite = unittest.TestSuite()
    suite.addTests([StatUtilTest])
    unittest.TextTestRunner(verbosity=2).run(suite)
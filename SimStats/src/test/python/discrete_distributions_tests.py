'''
@author: wrightm
@copyright: 2014 Michael Wright
@license: GNU GPLv3 http://www.gnu.org/licenses/gpl.html
'''

import unittest
from src.main.python.discrete_distributions import DictWrapper, Histogram, Pmf,\
    Cdf, make_hist_from_list, make_hist_from_dict, make_pmf_from_list,\
    make_pmf_from_dict, make_pmf_from_hist, make_pmf_from_cdf, make_mixture_pmfs,\
    make_cdf_from_dict, make_cdf_from_hist, make_cdf_from_pmf,\
    make_cdf_from_list, make_transform
import copy


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
        self.assertEqual(self.dct_wrapper, DictWrapper(d))
        
    def test_str_magic_method(self):
        self.assertEqual(str(self.dct_wrapper), "{0: 0.0, 1: 1.0, 2: 2.0, 3: 4.0}")

    def test_cmp_less_magic_method(self):
        self.assertEqual(cmp(self.dct_wrapper, DictWrapper({0:0.0,1:1.0,2:2.0,3:5.0})), -1)

    def test_cmp_more_magic_method(self):
        self.assertEqual(cmp(self.dct_wrapper, DictWrapper({0:0.0,1:1.0,2:2.0,3:3.0})), 1)
        
    def test_cmp_equal_magic_method(self):
        self.assertEqual(cmp(self.dct_wrapper, DictWrapper({0:0.0,1:1.0,2:2.0,3:4.0})), 0)
        
    def test_equal_magic_method(self):
        d = {0:0.0,1:1.0,2:2.0,3:4.0}
        self.dct_wrapper_2 = DictWrapper(d, name='test_wrapper')

        self.assertEqual((self.dct_wrapper == self.dct_wrapper_2), True)
        
    def test_ne_magic_method(self):
        d = {0:0.0,1:1.0,2:2.0,3:6.0}
        self.dct_wrapper_2 = DictWrapper(d, name='test_wrapper')

        self.assertEqual((self.dct_wrapper != self.dct_wrapper_2), True)
        
    def test_lt_magic_method(self):
        d = {0:0.0,1:1.0,2:2.0,3:6.0}
        self.dct_wrapper_2 = DictWrapper(d, name='test_wrapper')

        self.assertEqual((self.dct_wrapper < self.dct_wrapper_2), True)
        
    def test_gt_magic_method(self):
        d = {0:0.0,1:1.0,2:2.0,3:3.0}
        self.dct_wrapper_2 = DictWrapper(d, name='test_wrapper')

        self.assertEqual((self.dct_wrapper > self.dct_wrapper_2), True)
        
    def test_le_magic_method(self):
        d = {0:0.0,1:1.0,2:2.0,3:4.0}
        self.dct_wrapper_2 = DictWrapper(d, name='test_wrapper')

        self.assertEqual((self.dct_wrapper <= self.dct_wrapper_2), True)
        
    def test_ge_magic_method(self):
        d = {0:0.0,1:1.0,2:2.0,3:4.0}
        self.dct_wrapper_2 = DictWrapper(d, name='test_wrapper')

        self.assertEqual((self.dct_wrapper <= self.dct_wrapper_2), True)
        
    def test_pos_magic_method(self):
        d = {0:0.0,1:1.0,2:2.0,3:4.0}
        self.dct_wrapper_2 = DictWrapper(d, name='test_wrapper')

        self.assertEqual((+self.dct_wrapper == self.dct_wrapper_2), True)
        
    def test_neg_magic_method(self):
        d = {0:-0.0,1:-1.0,2:-2.0,3:-4.0}
        self.dct_wrapper_2 = DictWrapper(d, name='test_wrapper')

        self.assertEqual((-self.dct_wrapper == self.dct_wrapper_2), True)
    
    def test_sub_magic_method(self):
        d = {0:0.0,1:1.0,2:2.0,3:4.0}
        self.dct_wrapper_2 = DictWrapper(d, name='test_wrapper')

        self.assertEqual((self.dct_wrapper - self.dct_wrapper_2), DictWrapper({0:0.0,1:0.0,2:0.0,3:0.0}))
        
    def test_add_magic_method(self):
        d = {0:0.0,1:-1.0,2:-2.0,3:-4.0}
        self.dct_wrapper_2 = DictWrapper(d, name='test_wrapper')

        self.assertEqual((self.dct_wrapper + self.dct_wrapper_2), DictWrapper({0:0.0,1:0.0,2:0.0,3:0.0}))
            
    def test_mul_magic_method(self):
        d = {0:0.0,1:0.0,2:0.0,3:0.0}
        self.dct_wrapper_2 = DictWrapper(d, name='test_wrapper')

        self.assertEqual((self.dct_wrapper*self.dct_wrapper_2), DictWrapper({0:0.0,1:0.0,2:0.0,3:0.0}))

    def test_div_magic_method(self):
        d = {0:0.0,1:0.0,2:0.0,3:0.0}
        self.dct_wrapper_2 = DictWrapper(d, name='test_wrapper')

        self.assertEqual((self.dct_wrapper_2/self.dct_wrapper), DictWrapper({0:0.0,1:0.0,2:0.0,3:0.0}))

    def test_mod_magic_method(self):
        d = {0:0.0,1:0.0,2:0.0,3:0.0}
        self.dct_wrapper_2 = DictWrapper(d, name='test_wrapper')

        self.assertEqual((self.dct_wrapper_2%self.dct_wrapper), DictWrapper({0:0.0,1:0.0,2:0.0,3:0.0}))
    
    def test_pow_magic_method(self):
        d = {0:0.0,1:0.0,2:0.0,3:0.0}
        self.dct_wrapper_2 = DictWrapper(d, name='test_wrapper')
    
        self.assertEqual((self.dct_wrapper**self.dct_wrapper_2), DictWrapper({0:1.0,1:1.0,2:1.0,3:1.0}))

    def test_copy_magic_method(self):
        self.assertEqual(copy.copy(self.dct_wrapper), self.dct_wrapper)

    def test_deepcopy_magic_method(self):
        self.assertEqual(copy.deepcopy(self.dct_wrapper), self.dct_wrapper)
        
    def test_items(self):
        self.assertEqual(self.dct_wrapper.items(), [(0, 0.0), (1, 1.0), (2, 2.0), (3, 4.0)])

    def test_sort(self):
        self.assertEqual(self.dct_wrapper.sort(), [(0, 0.0), (1, 1.0), (2, 2.0), (3, 4.0)])

    def test_sort_zip(self):
        self.assertEqual(self.dct_wrapper.sort_zip(), [(0, 1, 2, 3), (0.0, 1.0, 2.0, 4.0)])

    def test_set(self):
        self.dct_wrapper[100] = 100
        self.assertEqual(self.dct_wrapper[100], 100)

        self.dct_wrapper.set(100, 1000)
        self.assertEqual(self.dct_wrapper[100], 1000)
        
    def test_get(self):
        self.assertEqual(self.dct_wrapper[0], 0.0)
        self.assertEqual(self.dct_wrapper.get(0), 0.0)
        self.assertEqual(self.dct_wrapper.get(10000, None), None)

    def test_increment(self):
        self.assertEqual(self.dct_wrapper.increment(0), 1.0)
        
    def test_multiply(self):
        self.assertEqual(self.dct_wrapper.multiply(0,1), 0.0)
     
    def test_divide(self):
        self.assertEqual(self.dct_wrapper.divide(0,1), 0.0)
    
    def test_mod(self):
        self.assertEqual(self.dct_wrapper.mod(0,1), 0.0)
    
    def test_is_subset(self):
        self.assertEqual(self.dct_wrapper.is_subset(DictWrapper({0:0.0,1:1.0,2:2.0,3:4.0})), True)
       
    def test_get_dict(self):
        self.assertEqual(self.dct_wrapper.get_dict(), {0:0.0,1:1.0,2:2.0,3:4.0})

    def test_get_values(self):
        self.assertEqual(self.dct_wrapper.get_keys(), [0,1,2,3])
        
    def test_get_total_entries(self):
        self.assertEqual(self.dct_wrapper.get_total_entries(), 7)
        
    def test_get_max_entry(self):
        self.assertEqual(self.dct_wrapper.get_max_entry(),4.0)
        
    def test_get_min_entry(self):
        self.assertEqual(self.dct_wrapper.get_min_entry(),0.0)
    

class HistogramTest(unittest.TestCase):
    
    def setUp(self):
        self.histo = Histogram()
        self.histo.increment(10)
        self.histo.increment(10)
        self.histo.increment(10)
        
    def tearDown(self):
        pass
    
    def test_get_frequency(self):
        self.assertEqual(self.histo.get_frequency(10), 3)
    
    def test_get_frequencies(self):
        self.assertEqual(self.histo.get_frequencies(), [10])
        
class PmfTest(unittest.TestCase):
    
    def setUp(self):
        self.pmf = Pmf(d={0:4.0,1:8.0,2:12.0,3:16.0})
        
    def test_get_prob(self):
        self.assertEqual(self.pmf.get_prob(0), 0.1)
        
    def test_get_probs(self):
        probs = self.pmf.get_probs()
        for indx, value in enumerate(probs):
            probs[indx] = round(value,1)
        self.assertEqual(probs, [0.1,0.2,0.3,0.4])
        
    def test_random(self):
        pmf = Pmf(d={0:10})
        self.assertEqual(pmf.random(), 0)
        
        
    def test_get_pmf_of_logs(self):
        probs = self.pmf.get_pmf_of_logs().get_probs()
        for indx, value in enumerate(probs):
            probs[indx] = round(value,1)

        self.assertEqual(probs, [-1.4,-0.7,-0.3,0.0])
        
    def test_get_pmf_of_exp(self):
        probs = self.pmf.get_pmf_of_exp().get_probs()
        for indx, value in enumerate(probs):
            probs[indx] = round(value,1)
            
        self.assertEqual(probs, [0.1,0.2,0.3,0.4])
        
    def test_max_likelihood(self):
        max_value, max_prob = self.pmf.max_likelihood()
        self.assertEqual(max_value, 3.0)
        self.assertEqual(max_prob, 0.4)
        
    def test_min_likelihood(self):
        min_value, min_prob = self.pmf.min_likelihood()
        self.assertEqual(min_value, 0.0)
        self.assertEqual(min_prob, 0.0)
        
class CdfTest(unittest.TestCase):
    
    def setUp(self):
        self.cdf = Cdf([(1,10.0),(2,20.0),(3,30.0),(4,40.0)], 'test_cdf')
        
    def test_cdf_constructor(self):
        self.assertEqual(self.cdf.sort(), [(1,0.1),(2,0.3),(3,0.6),(4,1.0)])
        
    def test_get_prob_with_key(self):
        self.assertEqual(self.cdf.get_prob(3), 0.6)
        
    def test_get_prob_without_key(self):
        self.assertEqual(self.cdf.get_prob(3.5), 0.6)

    def test_get_value_with_prob(self):
        self.assertEqual(self.cdf.get_value(0.6), 3)
        
    def test_get_value_without_prob(self):
        self.assertEqual(self.cdf.get_value(0.9), 3)

    def test_quantile(self):
        self.assertEqual(self.cdf.quantile(0.1),1)

    def test_percentile(self):
        self.assertEqual(self.cdf.percentile(10),1)
     
    def test_random(self):
        self.assertIn(self.cdf.random(), [1,2,3,4])
        
    def test_sample(self):
        self.assertEqual(len(self.cdf.sample(4)), 4)
        
class MakeMethodTest(unittest.TestCase):
    
    def test_make_hist_from_list_excep(self):
        lst = [1,1,2,2,3,3,4,5,5,5,5]
        self.assertRaises(TypeError, make_hist_from_list(lst))
        
    def test_make_hist_from_list(self):
        lst = [1,1,2,2,3,3,4,5,5,5,5]
        self.assertEqual(len(make_hist_from_list(lst)), 5)
        
    def test_make_hist_from_dict(self):
        dct = {1:2,2:2,3:3,4:1,5:4}
        self.assertEqual(len(make_hist_from_dict(dct)), 5)
        
    def test_make_pmf_from_list(self):
        lst = [1,1,2,2,3,3,4,5,5,5,5]
        self.assertEqual(len(make_pmf_from_list(lst)), 5)
                
    def test_make_pmf_from_dict(self):
        dct = {1:2,2:2,3:3,4:1,5:4}
        self.assertEqual(len(make_pmf_from_dict(dct)), 5)
        
    def test_make_pmf_from_hist(self):
        dct = {1:2,2:2,3:3,4:1,5:4}
        self.assertEqual(len(make_pmf_from_hist(Histogram(dct))), 5)
        
    def test_make_pmf_from_cdf(self):
        dct = {1:2,2:2,3:3,4:1,5:4}
        self.assertEqual(len(make_pmf_from_cdf(Cdf(Histogram(dct).sort()))), 5)
        
    def test_make_mixture_pmfs(self):
        dct = {1:2,2:2,3:3,4:1,5:4}
        pmfs = {Pmf(dct):0.1,Pmf(dct):0.2,Pmf(dct):0.3,Pmf(dct):0.4}
        self.assertEqual(len(make_mixture_pmfs(pmfs)),5)
      
    def test_make_cdf_from_items(self):
        dct = {1:2,2:2,3:3,4:1,5:4}
        items = Histogram(dct).sort()
        self.assertEqual(len(Cdf(items)), 5)
        
    def test_make_cdf_from_dict(self):
        dct = {1:2,2:2,3:3,4:1,5:4}
        self.assertEqual(len(make_cdf_from_dict(dct)),5 )
        
    def test_make_cdf_from_hist(self):
        dct = {1:2,2:2,3:3,4:1,5:4}
        self.assertEqual(len(make_cdf_from_hist(Histogram(dct))), 5)

    def test_make_cdf_from_pmf(self):
        dct = {1:2,2:2,3:3,4:1,5:4}
        self.assertEqual(len(make_cdf_from_pmf(Pmf(dct))), 5)
 
    def test_make_cdf_from_list(self):
        lst = [1,1,2,2,3,3,3,4,5,5,5]
        self.assertEqual(len(make_cdf_from_list(lst)), 5)
        
    def test_make_transform(self):
        dct = {1:2,2:2,3:3,4:1,5:4}
        old_pmf = Pmf(dct)
        new_pmf, options = make_transform(old_pmf)
        self.assertEqual(old_pmf, new_pmf)
        self.assertEqual(options, {'xscale':'linear','yscale':'linear'})
        
 
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    suite = unittest.TestSuite()
    suite.addTests([DictWrapperTest,HistogramTest, PmfTest, CdfTest, MakeMethodTest])
    unittest.TextTestRunner(verbosity=2).run(suite)
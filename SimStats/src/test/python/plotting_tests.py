'''
Created on 19 Jun 2014

@author: wrightm
'''
from src.main.python.plotting import add_options_to_plot, plot, save_format,\
    scatter_plot, hexbin_plot, plot_discrete_distribution, plot_histogram
from modulegraph import zipio
import unittest
import os
from src.main.python.discrete_distributions import Pmf


class PlottingTest(unittest.TestCase):


    def test_add_options_to_plot(self):
        self.assertEqual(add_options_to_plot(a='b', b='c'), {'a':'b','b':'c'})
        
    def test_plot(self):
        xs = [0,1,3,4,5]
        ys = [0,1,3,4,5]
        
        plot(xs,ys)
        filename  = '../resources/test_plot_method'
        save_format(filename)
        self.assertTrue(do_file_exist(filename+'.eps'))
        os.remove(filename+'.eps')
        
    def test_scatter_plot(self):
        xs = [0,1,3,4,5]
        ys = [0,1,3,4,5]
        
        scatter_plot(xs,ys)
        filename  = '../resources/test_scatter_plot_method'
        save_format(filename)
        self.assertTrue(do_file_exist(filename+'.eps'))
        os.remove(filename+'.eps')
        
    def test_hexbin_plot(self):
        xs = [0,1,3,4,5]
        ys = [0,1,3,4,5]
        
        hexbin_plot(xs,ys)
        filename  = '../resources/test_hexbin_plot_method'
        save_format(filename)
        self.assertTrue(do_file_exist(filename+'.eps'))
        os.remove(filename+'.eps')
    
    def test_plot_discrete_distribution(self):
        xs = [0,1,3,4,5]
        ys = [0,1,3,4,5]
        
        plot_discrete_distribution(Pmf(dict(zip(xs,ys))))
        filename  = '../resources/test_plot_discrete_distribution_method'
        save_format(filename)
        self.assertTrue(do_file_exist(filename+'.eps'))
        os.remove(filename+'.eps')
        
    def test_plot_histogram(self):
        xs = [0,1,3,4,5]
        ys = [0,1,3,4,5]
        
        plot_histogram(Pmf(dict(zip(xs,ys))))
        filename  = '../resources/test_plot_histogram_method'
        save_format(filename)
        self.assertTrue(do_file_exist(filename+'.eps'))
        os.remove(filename+'.eps')
        
def do_file_exist(filename):
    return zipio.isfile(filename)

if __name__ == "__main__":
    pass
    #import sys;sys.argv = ['', 'Test.testName']
    #suite = unittest.TestSuite()
    #suite.addTests([PlottingTest])
    #unittest.TextTestRunner(verbosity=2).run(suite)
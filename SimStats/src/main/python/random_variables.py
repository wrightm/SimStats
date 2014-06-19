'''
Created on 22 Apr 2014

@author: wrightm
'''
import random
import numpy.random
from src.main.python.discrete_distributions import make_pmf_from_list
from src.main.python.utils import test_obj_subclass


class RandomVariable(object):
    
    def generate(self):
        raise NotImplementedError()
    
class Exponential(RandomVariable):

    def __init__(self, lam):
        self.lam = lam

    def generate(self):
        return round(random.expovariate(self.lam),2)

class Erlang(RandomVariable):
    def __init__(self, lam, k):
        self.lam = lam
        self.k = k
        self.expo = Exponential(lam)
        
    def generate(self):
        total = 0
        for _ in xrange(self.k):
            total += round(self.expo.generate(), 2)
        return total
    
class Gumbel(RandomVariable):
    
    def __init__(self, mu, beta):
        self.mu = mu
        self.beta = beta
        
    def generate(self):
        return round(numpy.random.gumbel(self.mu, self.beta), 2)
    
class Normal(RandomVariable):
    
    def __init__(self, mu, sigma):
        self.mu = mu
        self.sigma = sigma
        
    def generate(self):
        return round(numpy.random.normal(self.mu, self.sigma),2)
    
class LogNormal(RandomVariable):
    
    def __init__(self, mu, sigma):
        self.mu = mu
        self.sigma = sigma   
    
    def generate(self):
        return round(numpy.random.lognormal(self.mu, self.sigma),2)
    
class Pareto(RandomVariable):
    
    def __init__(self, shape, mode):
        self.shape = shape
        self.mode = mode
    
    def generate(self):
        return round((numpy.random.pareto(self.shape, 1000) + self.mode),2)
    
class Sum(RandomVariable):
    
    def __init__(self, X, Y):
        self.X = X
        self.Y = Y
        test_obj_subclass(self.X, RandomVariable)
        test_obj_subclass(self.Y, RandomVariable)
        
    def generate(self):
        return round(self.X.generate() + self.X.generate(),2)
    
class Uniform(RandomVariable):
    
    def __init__(self, low, high, steps):
        self.low = low
        self.high = high
        self.steps = steps
        hypos = [self.low + (self.high-self.low) * i / (self.steps-1.0) for i in range(self.steps)]
        self.pmf = make_pmf_from_list(hypos)
        
    def generate(self):
        return self.pmf.random()
     
def generate_sample(rand_var, sample_size):
    
    if not issubclass(rand_var.__class__, RandomVariable):
        raise TypeError('Object rand_var is not of Subclass Type RandomVariable')
    return sorted([rand_var.generate() for _ in xrange(sample_size)])


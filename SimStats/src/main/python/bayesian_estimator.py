from src.main.python.utils import test_obj_instance, test_obj_subclass
from src.main.python.discrete_distributions import Pmf
from copy import deepcopy
from numpy.ma.core import exp


class Likelihood(object):
    
    def get_likelihood(self, evidence, hypothesis):
        raise NotImplementedError('Abstract Class, must implement abstract method.')

class ExponetialLikelihood(Likelihood):
    
    def get_likelihood(self, evidence, hypothesis):
        param = hypothesis
        likelihood = 1
        for x in evidence:
            likelihood *= param * exp(-param * x)
        return likelihood
    
class ConditionalExponetialLikelihood(Likelihood):
    
    def __init__(self, low, high):
        self.low = low
        self.high = high
        
    def get_likelihood(self, evidence, hypothesis):
        param = hypothesis
        likelihood = 1
        for x in evidence:
            factor = exp(-self.low * param) - exp(-self.high * param)
            likelihood *= param * exp(-param * x) / factor
        return likelihood

class LikelihoodOfSeeingASetOfNumberUpperBound(Likelihood):
    
    def get_likelihood(self, evidence, hypothesis):
        likelihood = 1.0    
        for x in evidence:
            if x > hypothesis:
                likelihood *= 0.0
                return likelihood
            else:
                likelihood *= 1.0 / hypothesis
            
        return likelihood
    
class LikelihoodOfSeeingASetOfNumberLowerBound(Likelihood):
    
    def get_likelihood(self, evidence, hypothesis):
        likelihood = 1.0    
        for x in evidence:
            if x < hypothesis:
                likelihood *= 0.0
                return likelihood
            else:
                likelihood *= 1.0 / hypothesis
            
        return likelihood
  
class BayesianEstimator(object):

    def __init__(self, prior, sample, likelihood):
        test_obj_instance(prior, Pmf)
        test_obj_instance(sample, list)
        test_obj_subclass(likelihood, Likelihood)
        self.prior = prior
        self.sample = sample
        self.likelihood = likelihood
        self.posterior = deepcopy(prior)
        self.posterior.name = 'posterior'
        self._estimate_posterior()
        
    def _estimate_posterior(self):
        dict.it
        for hypo in self.prior.get_dict().itervalues():
            self.posterior.multiply(hypo, self.likelihood.get_likelihood(self.sample,self.prior)) 
        self.posterior.normalise()
        
    def get_posterior(self):
        return self.posterior    
        
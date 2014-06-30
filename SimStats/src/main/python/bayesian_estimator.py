from src.main.python.utils import test_obj_instance, test_obj_subclass
from src.main.python.discrete_distributions import Pmf, make_pmf_from_list,\
    make_cdf_from_pmf
from copy import deepcopy
from numpy.ma.core import exp
from src.main.python.random_variables import Uniform


class Likelihood(object):
    
    def get_likelihood(self, evidence, hypothesis):
        raise NotImplementedError('Abstract Class, must implement abstract method.')

class ExponentialLikelihood(Likelihood):
    
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
            if not factor:
                likelihood *= 1
            else:
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
                if not hypothesis:
                    likelihood *= 1.0
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
                if not hypothesis:
                    likelihood *= 1.0
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
        for hypo in self.prior.get_dict().itervalues():
            self.posterior.multiply(hypo, self.likelihood.get_likelihood(self.sample,hypo)) 
        self.posterior.normalise()
        
    def get_posterior(self):
        return self.posterior  
      
if __name__ == '__main__':
    uniform = Uniform(0,100,100)
    uniform_dist = [uniform.generate() for _ in xrange(100)]
    prior = make_pmf_from_list(uniform_dist)
    sample = [10.0,9.0]
    bayesian_est = BayesianEstimator(prior, sample, ConditionalExponetialLikelihood(0,100))

    print make_cdf_from_pmf(bayesian_est.get_posterior()).sort()
        
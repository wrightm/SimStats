from src.main.python.stat_utils import chi_squared
from src.main.python.discrete_distributions import make_pmf_from_list, Pmf,\
    make_cdf_from_pmf
from src.main.python.utils import test_obj_instance, test_obj_subclass


class PmfProbabilities(object):
    
    def get_probabilities(self, pmf):
        raise NotImplementedError('abstract base class please implement method.')
    
class PmfProbabilityRange(PmfProbabilities):
    
    def __init__(self, low, high):
        self.low = low
        self.high = high
        
    def get_probabilities(self, pmf):
        test_obj_instance(pmf, Pmf)
        cdf = make_cdf_from_pmf(pmf)
        return cdf.get_prob(self.high) - cdf.get_prob(self.low)
    
class ChiSquaredTest(object):
    
    def __init__(self, observed_sample, expected_sample, prob_functions, ntrials=1000 ):
        self._validate_input_objects(observed_sample, expected_sample, prob_functions)
        
        self.expected_sample = expected_sample
        self.prob_functions = prob_functions
        self.ntrials = ntrials
        
        self.observed_probabilities = self._compute_probabilities(observed_sample)
        self.expected_probabilities = self._compute_probabilities(expected_sample)
    
        self.threshold = chi_squared(self.expected_probabilities, self.observed_probabilities)
        
        self.simulated_chi2s = self._compute_simulated_chi2()
        
        self.chi2s_greater_than_threshold = self._n_simulated_chi2s_greater_than_threshold()
        
    def _compute_probabilities(self, *samples):
        all_probs = []
        for sample in samples:
            probs = [prob_func(sample) for prob_func in self.prob_functions ]
            all_probs.append(probs)
        
        return all_probs
    
    def _simulate_probabilities(self):
        random_observed_sample = [self.expected_sample.random() for _ in xrange(len(self.expected_sample))]
        simulated_observed_sample = make_pmf_from_list(random_observed_sample, self.expected_sample.name)
        probs = [prob_func(simulated_observed_sample) for prob_func in self.prob_functions ]
        
        return [probs]
    
    def _compute_simulated_chi2(self):
        chi2s = []
        for _ in range(self.ntrials):
            simulated_probabilities = self._simulate_probabilities()
            chi2s.append(chi_squared(self.expected_probabilities, simulated_probabilities))
            
        return chi2s
    
    def _n_simulated_chi2s_greater_than_threshold(self):
        count = 0
        for chi in self.simulated_chi2s:
            if chi >= self.threshold:
                count += 1
        return count
    
    def get_expected_probabilities(self):
        return self.expected_probabilities
    
    def get_observed_probabilities(self):
        return self.observed_probabilities
    
    def get_threshold_chi2(self):
        return self.threshold
    
    def get_simulated_chi2s(self):
        return self.simulated_chi2s
    
    def get_pvalue(self):
        return 1.0 * self.chi2s_greater_than_threshold / self.ntrials
    
    def _validate_input_objects(self, observed_sample, expected_sample, prob_functions):
        test_obj_instance(observed_sample, Pmf)
        test_obj_instance(expected_sample, Pmf)


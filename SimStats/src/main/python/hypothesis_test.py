from src.main.python.utils import test_obj_instance
from src.main.python.discrete_distributions import Pmf, make_cdf_from_list
from src.main.python.stat_utils import partition_sample, difference_in_mean,\
    variance, sample_with_replacement
import math


class BayesianResult(object):
    
    def __init__(self, prior, posterior, likelihood, normalisation):
        self.prior = prior
        self.posterior = posterior
        self.likelihood = likelihood
        self.normalisation = normalisation
        
    def get_prior(self):
        return self.prior
    
    def get_posterior(self):
        return self.posterior
    
    def get_likelihood(self):
        return self.likelihood
    
    def get_normalisation(self):
        return self.normalisation
    
class BayesianResultSuite(object):
    
    def __init__(self, median_bayesian_result, plus_sigma_bayesian_result, minus_sigma_bayesian_result):
        test_obj_instance(median_bayesian_result, BayesianResult)
        test_obj_instance(plus_sigma_bayesian_result, BayesianResult)
        test_obj_instance(minus_sigma_bayesian_result, BayesianResult)
        
        self.median_bayesian_result = median_bayesian_result
        self.plus_sigma_bayesian_result = plus_sigma_bayesian_result
        self.minus_sigma_bayesian_result = minus_sigma_bayesian_result
        
    def get_median_bayesian_result(self):
        return self.median_bayesian_result
    
    def get_plus_sigma_bayesian_result(self):
        return self.plus_sigma_bayesian_result
    
    def get_minus_sigma_bayesian_result(self):
        return self.minus_sigma_bayesian_result
    
class HypoTestResult(object):
    
    def __init__(self, results):
        test_obj_instance(results, dict)
        self.results = results
        
    def get_median_pvalue(self):
        return self.results.get('median_pvalue', 0.0)
    
    def get_median_right_tail(self):
        return self.results.get('median_right_tail', 0.0)
    
    def get_median_left_tail(self):
        return self.results.get('median_left_tail', 0.0)
    
    def get_plus_one_sigma_pvalue(self):
        return self.results.get('plus_one_sigma_pvalue', 0.0)
    
    def get_plus_one_sigma_right_tail(self):
        return self.results.get('plus_one_sigma_right_tail', 0.0)
    
    def get_plus_one_sigma_left_tail(self):
        return self.results.get('plus_one_sigma_left_tail', 0.0)
    
    def get_minus_one_sigma_pvalue(self):
        return self.results.get('minus_one_sigma_pvalue', 0.0)
    
    def get_minus_one_sigma_right_tail(self):
        return self.results.get('minus_one_sigma_right_tail', 0.0)
    
    def get_minus_one_sigma_left_tail(self):
        return self.results.get('minus_one_sigma_left_tail', 0.0)


class HypoResultSuite(object):
    
    def __init__(self, null_hypo_results, alternative_hypo_result, bayesian_result_suite):
        test_obj_instance(null_hypo_results, HypoTestResult)
        test_obj_instance(alternative_hypo_result, HypoTestResult)
        test_obj_instance(bayesian_result_suite, BayesianResultSuite)
        
        self.null_hypo_results = null_hypo_results
        self.alternative_hypo_result = alternative_hypo_result
        self.bayesian_result_suite = bayesian_result_suite
        
    def get_null_hypo_results(self):
        return self.null_hypo_results
    
    def get_alternative_hypo_result(self):
        return self.alternative_hypo_result
    
    def get_bayesian_result_suite(self):
        return self.bayesian_result_suite

class HypothesisTest(object):
    
    def __init__(self, sample_one, sample_two, population, options):
        self.sample_one = sample_one
        self.sample_two = sample_two
        self.population = population
        self.options = options

        self._validate_objects()
        
        sample_one.sort()
        sample_two.sort()
        population.sort()
        self.nitems_sample_one = len(self.sample_one)
        self.nitems_sample_two = len(self.sample_two)
        
        self.partition = self.options.get('partition', False)
        self.prior = self.options.get('prior', 1.0)
        self.trials = self.options.get('trials', 1000)
        
        self.model_one = self.sample_one
        self.model_two = self.sample_two

        if self.partition:
            self.sample_one, self.model_one = partition_sample(self.sample_one, self.nitems_sample_one/2)
            self.sample_two, self.model_two = partition_sample(self.sample_two, self.nitems_sample_two/2)

    def run_test(self):
        
        # P(E|H0), prob of effect being greater or equal given the null hypothesis
        peh0 = self.test(self.sample_one, self.sample_two, self.population, self.population)
        
        # P(E|Ha), prob of effect being greater or equal given the alternative hypothesis
        # Probability of seeing the effect given the effect is real
        peha = self.test(self.sample_one, self.sample_two, self.model_one, self.model_two)
        
        #
        # P(Ha|E) posterior - the probability the effect is real given the effect
        # P(Ha) prior - the probability of the effect being real before seeing the effect
        # P(E) probability of seeing the effect under any hypothesis
        pha = self.prior
        # median
        median_pe = pha*peha.get_median_pvalue() + (1.0-pha)*peh0.get_median_pvalue()
        median_phae = pha*peha.get_median_pvalue() / median_pe
        median_bayesian_result = BayesianResult(pha, median_phae, peha.get_median_pvalue(), median_pe)
        # plus sigma
        plus_one_sigma_pe = pha*peha.get_plus_one_sigma_pvalue() + (1.0-pha)*peh0.get_plus_one_sigma_pvalue()
        plus_one_sigma_phae = pha*peha.get_plus_one_sigma_pvalue() / plus_one_sigma_pe
        plus_one_sigma_bayesian_result = BayesianResult(pha, plus_one_sigma_phae, peha.get_plus_one_sigma_pvalue(), plus_one_sigma_pe)
        # minus sigma
        minus_one_sigma_pe = pha*peha.get_minus_one_sigma_pvalue() + (1.0-pha)*peh0.get_minus_one_sigma_pvalue()
        minus_one_sigma_phae = pha*peha.get_minus_one_sigma_pvalue() / minus_one_sigma_pe
        minus_one_sigma_bayesian_result = BayesianResult(pha, minus_one_sigma_phae, peha.get_minus_one_sigma_pvalue(), minus_one_sigma_pe)
    
        bayesian_result_suite = BayesianResultSuite(median_bayesian_result, plus_one_sigma_bayesian_result, minus_one_sigma_bayesian_result)
    
        return HypoResultSuite(peh0, peha, bayesian_result_suite)
    
    def test(self, sample_one, sample_two, model_one, model_two):
        raise NotImplementedError('HypothesisTest is a abstract base class. please implement abstract method')
    
    def _validate_objects(self):
        test_obj_instance(self.sample_one, list)
        test_obj_instance(self.sample_two, list)
        test_obj_instance(self.population, list)
        test_obj_instance(self.options, dict)
        
class HypothesisTestDifferenceInMean(HypothesisTest):
    
    def __init__(self, sample_one, sample_two, population, options):
        super(HypothesisTestDifferenceInMean, self).__init__(sample_one, sample_two, population, options)
        
    def test(self, sample_one, sample_two, model_one, model_two):
        mu_sample_one, mu_sample_two, delta = difference_in_mean(sample_one, sample_two)
        delta = abs(delta)
        var_sample_one = variance(sample_one, mu_sample_one)
        var_sample_two = variance(sample_two, mu_sample_two)
        delta_std_dev = math.fabs(math.sqrt((var_sample_one/self.nitems_sample_one) + (var_sample_two/self.nitems_sample_two)))
        
        median_pvalue, median_left_tail, median_right_tail = self.pvalue(model_one, model_two, delta)
        plus_one_sigma_pvalue, plus_one_sigma_left_tail, plus_one_sigma_right_tail = self.pvalue(model_one, model_two, delta+delta_std_dev)
        minus_one_sigma_pvalue, minus_one_sigma_left_tail, minus_one_sigma_right_tail = self.pvalue(model_one, model_two, delta-delta_std_dev)
        
        results = { 'median_pvalue': median_pvalue,
                    'median_left_tail': median_left_tail,
                    'median_right_tail': median_right_tail,
                    'plus_one_sigma_pvalue': plus_one_sigma_pvalue, 
                    'plus_one_sigma_left_tail': plus_one_sigma_left_tail,
                    'plus_one_sigma_right_tail': plus_one_sigma_right_tail,
                    'minus_one_sigma_pvalue': minus_one_sigma_pvalue,
                    'minus_one_sigma_left_tail': minus_one_sigma_left_tail,
                    'minus_one_sigma_right_tail': minus_one_sigma_right_tail }
        
        return HypoTestResult(results)    
    
    def pvalue(self, model_one, model_two, delta_from_sample):
        deltas = [self._resample(model_one, model_two) for _ in xrange(self.trials)]
        
        cdf_deltas = make_cdf_from_list(deltas)
        
        left_tail = cdf_deltas.get_prob(-delta_from_sample)
        right_tail = cdf_deltas.get_prob(delta_from_sample)
        pvalue = left_tail + right_tail
        
        return pvalue, left_tail, right_tail
        
    def _resample(self, model_one, model_two):
        sample_one = sample_with_replacement(model_one, len(model_one))
        sample_two = sample_with_replacement(model_two, len(model_two))
        _, _, delta = difference_in_mean(sample_one, sample_two)
        return delta
        
'''
@author: wrightm
@copyright: 2014 Michael Wright
@license: GNU GPLv3 http://www.gnu.org/licenses/gpl.html
'''
from src.main.python.discrete_distributions import Histogram, Pmf, Cdf,\
    make_cdf_from_hist, make_cdf_from_pmf, make_cdf_from_list

import math
import itertools
import random
from src.main.python.utils import test_obj_instance

def mean(obj):
    mu = 0.0
    if isinstance(obj, Histogram):
        for x, count in obj:
            mu += x * count
        return mu / obj.get_total_entries()
    elif isinstance(obj, Pmf):
        for x, p in obj:
            mu += p * x
        return mu
    elif isinstance(obj, Cdf):
        old_p = 0.0
        for x, p in obj:
            p -= old_p
            mu += p * x
            old_p = p
        return mu
    elif isinstance(obj, list) or hasattr(obj, '__itr__'):
        return float(sum(obj)) / len(obj)
    else:
        raise TypeError('object must be of dict, list, histogram or Pmf type.')

def median(obj):
    if isinstance(obj, Histogram):
        cdf = make_cdf_from_hist(obj)
        return cdf.get_value(0.5)
    elif isinstance(obj, Pmf):
        cdf = make_cdf_from_pmf(obj)
        return cdf.get_value(0.5)
    elif isinstance(obj, Cdf):
        return obj.get_value(0.5)
    elif isinstance(obj, list) or hasattr(obj, '__itr__'):
        cdf = make_cdf_from_list(obj)
        return cdf.get_value(0.5)
    else:
        raise TypeError('object must be of dict, list, histogram or Pmf type.')
      
def variance(obj, mu=None):
    if mu is None:
        mu = mean(obj)
    
    var = 0.0
    if isinstance(obj, Histogram):
        for x, count in obj:
            var += count * (x-mu)**2
        return var / obj.get_total_entries()
    if isinstance(obj, Pmf):
        for x, p in obj:
            var += p * (x-mu)**2
        return var
    elif isinstance(obj, Cdf):
        old_p = 0.0
        for x, p in obj:
            p -= old_p
            var += p * (x-mu)**2
            old_p = p
        return var
    elif isinstance(obj, list) or hasattr(obj, '__itr__'):
        for x in obj:
            var += (x-mu)**2
        return var / len(obj)
    else:
        raise TypeError('obj must be of dict, list, histogram, Pmf or Cdf type.')
    
def standard_dev(obj, mu=None):
    return math.sqrt(variance(obj, mu))

def zscores(obj, mu=None, sigma=None):

    if mu is None:
        mu = mean(obj)
    if sigma == None:
        sigma = standard_dev(obj, mu)
        
    z_scores = []
    if isinstance(obj, (Histogram,Pmf,Cdf)):
        for x, _ in obj.sort():
            z_scores.append(zscore(x, mu, sigma)) 
    elif isinstance(obj, list) or hasattr(obj, '__itr__'):
        for x in sorted(obj):
            z_scores.append(zscore(x, mu, sigma))
    else:
        raise TypeError('obj must be of dict, list, histogram, Pmf or Cdf type.')
  
    return z_scores

def zscore(x, mu, sigma):
    if sigma == 0:
        return 0.0
    return (x - mu) / sigma

def zscores_correlation(obj1, obj2):

    zscores_obj1 = zscores(obj1)
    zscores_obj2 = zscores(obj2)
    
    return correlation(zscores_obj1, zscores_obj2)
        
def covariance(xs, ys, mux=None, muy=None):
    
    if mux == None:
        mux = mean(xs)
    if muy == None:
        muy = mean(ys)
        
    total = 0.0
    for x, y in zip(xs, ys):
        total += (x-mux) * (y-muy)
        
    return total / len(xs)

def correlation(xs, ys):
    
    mux = mean(xs)
    muy = mean(ys)
    
    sigma_x = standard_dev(xs, mux)
    sigma_y = standard_dev(ys, muy)

    if not sigma_x or not sigma_y:
        return 0.0
    return covariance(xs, ys, mux, muy) / (sigma_x * sigma_y)

def serial_correlation(xs):
    return correlation(xs[:-1], xs[1:])

def spearman_correlation(xs, ys):
    xranks = ranks(xs)
    yranks = ranks(ys)
    return correlation(xranks, yranks)

def ranks(lst):
    # index list
    enumerated_list = enumerate(lst)
    # sort list by list values
    sorted_enumerated_list = sorted(enumerated_list, key=lambda pair: pair[1])
    # index sorted list 
    rank_sorted_enumerated_list = enumerate(sorted_enumerated_list)
    # sort index list by value 
    rank_resorted_enumerated_list = sorted(rank_sorted_enumerated_list, key=lambda tup: tup[1][0])
    # put ranks into a list
    rnks = [trip[0]+1 for trip in rank_resorted_enumerated_list]
    return rnks
    
def differences_adj_elements(lst):
    if not isinstance(lst, (list,tuple)):
        raise TypeError('lst object is not of Type list')
    
    return [lst[i+1]-lst[i] for i in xrange(len(lst)-1)]

def chi_squared(expected, observed):
    it = zip(itertools.chain(*expected), 
             itertools.chain(*observed))
    t = [(obs - exp)**2 / exp for exp, obs in it]
    return sum(t)

def sample_with_replacement(sample, sample_size):
    return [random.choice(sample) for _ in xrange(sample_size)]

def sample_without_replacement(sample, sample_size):
    return random.sample(sample, sample_size)

def partition_sample(sample, sample_split):
    random.shuffle(sample)
    return sample[:sample_split], sample[sample_split:]

def difference_in_mean(sample1, sample2):
    mu1 = mean(sample1)
    mu2 = mean(sample2)
    delta = mu1 - mu2

    return mu1, mu2, delta

def relative_mean_difference(pmf, mu=None):
    test_obj_instance(pmf, Pmf)
    if mu is None:
        mu = mean(pmf)

    diff = Pmf()
    for v1, p1 in pmf.items():
        for v2, p2 in pmf.items():
            diff.increment(abs(v1-v2), p1*p2)

    return mean(diff) / mu




    
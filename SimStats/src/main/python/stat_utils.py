'''
@author: wrightm
@copyright: 2014 Michael Wright
@license: GNU GPLv3 http://www.gnu.org/licenses/gpl.html
'''
from src.main.python.discrete_distributions import Histogram, Pmf, Cdf

import math

def mean(obj):
    mu = 0.0
    if isinstance(obj, Histogram) or isinstance(obj, Pmf):
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
        return float(sum(obj)) / (len(obj) - 1)
    else:
        raise TypeError('object must be of dict, list, histogram or Pmf type.')
    
def variance(obj, mu=None):
    if mu is None:
        mu = mean(obj)
    
    var = 0.0
    if isinstance(obj, Histogram) or isinstance(obj, Pmf):
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
        return var
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
    if isinstance(obj, (Histogram,Pmf)):
        for x, p in obj.sort():
            z_scores.append(zscore(p, mu, sigma)) 
    elif isinstance(obj, Cdf):
        old_p = 0.0
        for x, p in obj.sort():
            p -= old_p
            old_p = p
            z_scores.append(zscore(p, mu, sigma))
    elif isinstance(obj, list) or hasattr(obj, '__itr__'):
        for x in sorted(obj):
            z_scores.append(zscore(x, mu, sigma))
    else:
        raise TypeError('obj must be of dict, list, histogram, Pmf or Cdf type.')
  
    return z_scores

def zscore(x, mu, sigma):
    return (x - mu) / sigma

def zscores_correlation(obj1, obj2):

    zscores_obj1 = zscore(obj1)
    zscores_obj2 = zscore(obj2)
    
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
    
    if not isinstance(lst, list):
        raise TypeError('lst object is not of Type list')
    
    return [lst[i+1]-lst[i] for i in xrange(len(lst)-1)]


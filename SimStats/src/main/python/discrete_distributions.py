'''
@author: wrightm
@copyright: 2014 Michael Wright
@license: GNU GPLv3 http://www.gnu.org/licenses/gpl.html
'''

import logging
import math
import random
import copy

class DictWrapper(object):

    def __init__(self, d=None, name=''):
        if d == None:
            d = {}
            
        self._testObjectType(d)
        self.d = d
        self.name = name

    def __delitem__(self, x):
        if self.d.has_key(x):
            del self.d[x]
            
    def __getitem__(self, key):
        return self.d.get(key)
    
    def __contains__(self, item):
        return self.d.has_key(item)
    
    def __len__(self):
        return len(self.d)
    
    def __iter__(self):
        return iter(self.d.iteritems())
    
    def __str__(self):
        return str(self.d)
    
    def __cmp__(self, other):
        self._testObjectType(other)
        if self.d < other:
            return -1
        elif self.d > other:
            return 1
        elif self.d == other:
            return 0
        
    def __eq__(self, other):
        self._testObjectType(other)
        return (self.d == other)    
    
    def __ne__(self, other):
        self._testObjectType(other)
        return (self.d != other)
    
    def __lt__(self, other):
        self._testObjectType(other)
        return (self.d < other)

    def __gt__(self, other):
        self._testObjectType(other)
        return (self.d > other)
    
    def __le__(self, other):
        self._testObjectType(other)
        return (self.d <= other)
    
    def __ge__(self, other):
        self._testObjectType(other)
        return (self.d >= other)
    
    def __pos__(self):
        return DictWrapper(self.d, self.name)
    
    def __neg__(self):
        d = {}
        for key, value in self.d.iteritems():
            d[key] = -value
        return DictWrapper(d, self.name)
    
    def __round__(self, n):
        d = {}
        for key, value in self.d.iteritems():
            d[key] = round(value, n)
        return DictWrapper(d, self.name)

    def __add__(self, other):
        d = copy.deepcopy(self.d)
        for key, value in self.other.iteritems():
            d[key] += value
        return DictWrapper(d, self.name)
        
    def __sub__(self, other):
        d = copy.deepcopy(self.d)
        for key, value in self.other.iteritems():
            d[key] -= value
        return DictWrapper(d, self.name)
    
    def __mul__(self, other):
        d = copy.deepcopy(self.d)
        for key, value in self.other.iteritems():
            d[key] *= value
        return DictWrapper(d, self.name)
    
    def __div__(self, other):
        d = copy.deepcopy(self.d)
        for key, value in self.other.iteritems():
            if value == 0.0:
                d[key] = 0
            else:
                d[key] /= value
        return DictWrapper(d, self.name)
    
    def __mod__(self, other):
        d = copy.deepcopy(self.d)
        for key, value in self.other.iteritems():
            d[key] %= value
        return DictWrapper(d, self.name)

    def __pow__(self, other):
        d = copy.deepcopy(self.d)
        for key, value in self.other.iteritems():
            d[key] = d[key]**value
        return DictWrapper(d, self.name)
    
    def __copy__(self):
        return DictWrapper(copy.copy(self.d), copy.copy(self.name))
    
    def __deepcopy__(self, memo):
        return DictWrapper(copy.deepcopy(self.d), copy.deepcopy(self.name))
    
    def _testObjectType(self, obj):
        if not isinstance(obj, dict) and not issubclass(obj, dict):
            raise TypeError('object must be of type dict or subclass of dict')
        
    def items(self):
        return self.d.items()

    def sort(self):
        return zip(*sorted(self.items()))

    def set(self, x, y=0):
        self.d[x] = y
        
    def get(self, x, default=None):
        return self.d.get(x,default)

    def increment(self, x, term=1):
        self.d[x] = self.d.get(x, 0) + term

    def multiply(self, x, factor):
        self.d[x] = self.d.get(x, 0) * factor
    
    def is_subset(self, other):
        for val, freq in self.Items():
            if freq > other[val]:
                return False
        return True
    
    def get_dict(self):
        return self.d

    def get_values(self):
        return self.d.keys()
        
    def get_total_entries(self):
        return sum(self.d.itervalues())

    def get_max_entry(self):
        return max(self.d.itervalues())

    def get_min_entry(self):
        return min(self.d.itervalues())
    
class Histogram(DictWrapper):

    def __init__(self, d=None, name=''):
        super(Histogram, self).__init__(d, name)

    def get_frequency(self, value, default=0):
        return self.get(value, default)
    
    def get_frequencies(self):
        return self.get_values()


class Pmf(DictWrapper):
    
    def __init__(self, d=None, name=''):
        super(Pmf, self).__init__(d, name)

    def get_prob(self, x, default=0):
        return self.get(x, default)

    def get_probs(self):
        return self.get_values()

    def normalise(self, fraction=1.0):
        total = self.total()
        if total == 0.0:
            logging.warning('Normalize: total probability is zero.')
            raise ValueError('total probability is zero.')
        
        factor = float(fraction) / total
        for x in self.d:
            self.d[x] *= factor
    
    def random(self):
        if len(self.d) == 0:
            raise ValueError('Pmf contains no values.')
            
        target = random.random()
        total = 0.0
        for x, p in self.d.iteritems():
            total += p
            if total >= target:
                return x
    
    def get_pmf_of_logs(self):
        m = self.max_likelihood()[1]
        for x, p in self.d.iteritems():
            self.Set(x, math.log(p/m))

    
    def get_pmf_of_exp(self):
        m = self.max_likelihood()[1]
        for x, p in self.d.iteritems():
            self.Set(x, math.exp(p-m))

    def max_likelihood(self):
        max_value = 0.0
        max_prob = 0.0
        for x, p in self.d.iteritems():
            if p > max_prob:
                max_prob = p
                max_value = x
                
        return max_value, max_prob
    
    def min_likelihood(self):
        min_value = 0.0
        min_prob = 0.0
        for x, p in self.d.iteritems():
            if p < min_prob:
                min_prob = p
                min_value = x
                
        return min_value, min_prob
        
         
class Cdf(DictWrapper):
    
    def __init__(self, d={}, name=''):
        super(Cdf, self).__init__(d, name) 
        
    def get_prob(self, x):
        
        if self.d.has_key(x):
            return self.d[x]
        
        values_probs = self.sort()
        last_prob = values_probs[0][1]
        for value, prob in values_probs:
            if value > x:
                return last_prob
            last_prob = prob
            
        last_value_prob_indx = len(values_probs) - 1
        
        return values_probs[last_value_prob_indx][1]
        
    def get_value(self, p):
        
        values_probs = self.sort()
        last_value = values_probs[0][0]
        for value, prob in values_probs:
            if prob > p:
                return last_value
            last_value = value

        last_value_prob_indx = len(values_probs) - 1
        
        return values_probs[last_value_prob_indx][0]
    
    def quantile(self, quant):
        
        return self.get_value(quant)
    
    def percentile(self, p):
        
        return self.get_value(p/100.0)
    
    def random(self):
        
        return self.get_value(random.random())

    def sample(self, n, name=''):
 
        d = {}       
        for _ in range(n):
            value = self.random()
            d[value] = self.get_prob(value)
            
        return Cdf(d, name)
        
def make_hist_from_list(lst, name=''):
    if not isinstance(lst, list):
        raise TypeError('lst object must be of type list')
    
    hist = Histogram(name=name)
    [hist.increment(x) for x in lst]
    return hist


def make_hist_from_dict(dct, name=''):
    if not isinstance(dct, dict):
        raise TypeError('dct object must be of type dict')
    
    return Histogram(dct, name)


def make_pmf_from_list(lst, name=''):
    if not isinstance(lst, list):
        raise TypeError('lst object must be of type list')
    
    hist = make_hist_from_list(lst, name)
    return make_pmf_from_hist(hist)


def make_pmf_from_dict(dct, name=''):
    if not isinstance(dct, dict):
        raise TypeError('dct object must be of type dict')
    
    pmf = Pmf(dct, name)
    pmf.normalise()
    return pmf


def make_pmf_from_hist(hist, name=None):
    if name is None:
        name = hist.name

    if not isinstance(hist, Histogram):
        raise TypeError('hist object must be of type Histogram')
    # make a copy of the dictionary
    d = dict(hist.get_dict())
    pmf = Pmf(d, name)
    pmf.normalise()
    return pmf


def make_pmf_from_cdf(cdf, name=None):
    if name is None:
        name = cdf.name

    if not isinstance(cdf, Cdf):
        raise TypeError('cdf object must be of type Cdf')
        
    pmf = Pmf(name=name)

    prev = 0.0
    for val, prob in cdf:
        pmf.increment(val, prob-prev)
        prev = prob

    return pmf


def make_mixture_pmfs(pmfs, name='mix'):
    if not isinstance(pmfs, dict):
        raise TypeError('pmfs object must be of type dict')
    
    mix = Pmf(name=name)
    for pmf, prob in pmfs:
        if not isinstance(pmf, (Pmf,Histogram)):
            raise TypeError('pmf object must be of type Pmf or Histogram')
        for x, p in pmf:
            mix.increment(x, p * prob)
    return mix

def make_cdf_from_items(items, name):
    runsum = 0
    d = {}
    items = sorted(items)
    for value, count in items:
        runsum += count
        d[value] = runsum

    total = float(runsum)
    for value, count in items:
        d[value] = d[value]/total

    cdf = Cdf(d, name)
    return cdf

def make_cdf_from_dict(dct, name=''):
    if not isinstance(dct, dict):
        raise TypeError('dct object must be of type dict')
    
    return make_cdf_from_items(dct.iteritems(), name)

def make_cdf_from_hist(hist, name=None):
    if name == None:
        name = hist.name
    
    return make_cdf_from_items(hist.items(), name)

def make_cdf_from_pmf(pmf, name=None):
    if name == None:
        name = pmf.name
        
    return make_cdf_from_items(pmf.items(), name)

def make_cdf_from_list(seq, name=''):
    hist = make_hist_from_list(seq)
    return make_cdf_from_hist(hist, name)

def make_transform(distro, transform_type, complement=False):
    
    if not issubclass(distro, DictWrapper):
        raise TypeError('distro is not of subclass DictWrapper')
    
    xs, ps = distro.sort()
    scale = dict(xscale='linear', yscale='linear')

    if transform_type == 'exponential':
        complement = True
        scale['yscale'] = 'log'

    if transform_type == 'pareto':
        complement = True
        scale['yscale'] = 'log'
        scale['xscale'] = 'log'

    if complement:
        ps = [1.0-p for p in ps]

    if transform_type == 'weibull':
        xs.pop()
        ps.pop()
        ps = [-math.log(1.0-p) for p in ps]
        scale['xscale'] = 'log'
        scale['yscale'] = 'log'

    if transform_type == 'gumbel':
        xs.pop(0)
        ps.pop(0)
        ps = [-math.log(p) for p in ps]
        scale['yscale'] = 'log'
    
    return distro.__class__(dict(zip(xs,ps)), distro.name), scale
        
        
    
    
    
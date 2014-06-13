'''
@author: wrightm
@copyright: 2014 Michael Wright
@license: GNU GPLv3 http://www.gnu.org/licenses/gpl.html
'''
from src.main.python.stat_utils import mean, variance, covariance
from src.main.python.discrete_distributions import make_pmf_from_dict

class LeastSquares(object):

    def __init__(self, xs, ys):
        self.xs = xs
        self.ys = ys
        
        self.mux = mean(self.xs)
        self.muy = mean(self.ys)
        
        self.varx = variance(self.xs, self.mux)
        self.vary = variance(self.xy, self.muy)
        
    def fit_line(self):
        grad = self.gradient()
        inter = self.intercept()
        ys = [(x*grad) + inter for x in self.xs]
        return self.xs, ys
    
    def fit_line_pmf(self, name=''):
        dct = dict(zip(self.fit_line()))
        return make_pmf_from_dict(dct)
    
    def gradient(self):
        return covariance(self.xs, self.ys, self.mux, self.muy) / self.varx
    
    def intercept(self):
        return self.muy - (self.gradient()*self.mux)
    
    def residuals(self):
        return [y - self.intercept() - (self.gradient()*x) for x, y in zip(self.xs, self.ys)]
    
    def coefficient_of_determination(self):
        res = self.residuals()
        varres = variance(res)
        return 1 - varres / self.vary
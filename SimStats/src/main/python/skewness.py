from src.main.python.stat_utils import median, mean
from src.main.python.utils import test_obj_instance
import math

class Skewness(object):
    
    def __init__(self, sample):
        test_obj_instance(sample, list)
        self.__sample = sample
        self.__mean = mean(sample)
        self.__median = median(sample)
        
    def _m2(self):
        """
        Mean Squared Deviation (Variance)
        """
        n = float(len(self.__sample))
        sum_squared = sum(math.pow(x - self.__mean, 2) for x in self.__sample)
        return sum_squared / n
    
    def _m3(self):
        """
        Mean Cubed Deviation
        """
        n = float(len(self.__sample))
        sum_squared = sum(math.pow(x - self.__mean, 3) for x in self.__sample)
        return sum_squared / n
    
    def g1(self):
        """
        basic skeweness, bias to outliers.
        
        -ve skewness. skews left
        +ve skewness. skews right
        """
        if self._m2() == 0.0:
            return 0.0
        return self._m3() / math.sqrt(math.pow(self._m2(), 3))
    
    def gp(self):
        """
        Pearson's median skewness coefficient
        """
        sigma = math.sqrt(self._m2())
        if sigma == 0.0:
            return 0.0
        return (3.0*(self.__mean - self.__median)) / sigma

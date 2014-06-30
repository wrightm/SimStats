import unittest
from src.main.python.skewness import Skewness

class SkewnessTest(unittest.TestCase):
    
    def setUp(self):
        self.skewness = Skewness([1,1,1,1,1,1,1,1,1,1])
        
    def test_m2(self):
        self.assertEqual(self.skewness._m2(), 0.0)
        
    def test_m3(self):
        self.assertEqual(self.skewness._m3(), 0.0)
        
    def test_g1(self):
        self.assertEqual(self.skewness.g1(), 0.0)
        
    def test_gp(self):
        self.assertEqual(self.skewness.gp(), 0.0)
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    suite = unittest.TestSuite()
    suite.addTests([])
    unittest.TextTestRunner(verbosity=2).run(suite)
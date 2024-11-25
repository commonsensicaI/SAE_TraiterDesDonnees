import unittest
from analyse_gps import analyser_trame

class TestAnalyseGPS(unittest.TestCase):

    def test_analyser_trame(self):
        positions, calculs = analyser_trame('data/trame_gps.log')
        self.assertTrue(len(positions) > 0)
        self.assertIn('max_lat', calculs)

if __name__ == '__main__':
    unittest.main()

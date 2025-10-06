import unittest
from _internal.invariant_factors import *


class TestFactors(unittest.TestCase):
    def test_prime_factors_prime(self):
        self.assertEqual(prime_factors(13), {13: 1})

    def test_prime_factors_large_prime(self):
        self.assertEqual(prime_factors(9973), {9973: 1})

    def test_prime_factors_composite(self):
        self.assertEqual(prime_factors(12), {2: 2, 3: 1})

    def test_prime_factors_large_composite(self):
        self.assertEqual(prime_factors(999), {3: 3, 37: 1})

    def test_prime_factors_power(self):
        self.assertEqual(prime_factors(1024), {2: 10})

    def test_invariant_factors_one_number(self):
        self.assertEqual(invariant_factors([100]), [100])

    def test_invariant_factors_equal_numbers(self):
        self.assertEqual(invariant_factors([8, 8, 8]), [8, 8, 8])

    def test_invariant_factors_distinct_prime_powers(self):
        self.assertEqual(invariant_factors([2, 4, 8]), [2, 4, 8])

    def test_invariant_factors_distinct_composites(self):
        self.assertEqual(invariant_factors([4, 6, 9, 10]), [2, 6, 180])


if __name__ == '__main__':
    unittest.main()

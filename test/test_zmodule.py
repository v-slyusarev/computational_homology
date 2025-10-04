import unittest
from homology.zmodule import FinitelyGeneratedZModule


class TestStringMethods(unittest.TestCase):
    def test_printing_0(self):
        module = FinitelyGeneratedZModule(0, [])
        self.assertEqual(str(module), '0')

    def test_printing_Z(self):
        module = FinitelyGeneratedZModule(1, [])
        self.assertEqual(str(module), 'ℤ')

    def test_printing_Z_with_rank(self):
        module = FinitelyGeneratedZModule(5, [])
        self.assertEqual(str(module), 'ℤ^5')

    def test_printing_cyclic(self):
        module = FinitelyGeneratedZModule(0, [2])
        self.assertEqual(str(module), 'ℤ/2ℤ')

    def test_printing_torsion(self):
        module = FinitelyGeneratedZModule(0, [2, 4])
        self.assertEqual(str(module), 'ℤ/2ℤ ⊕ ℤ/4ℤ')

    def test_printing_all(self):
        module = FinitelyGeneratedZModule(5, [2, 2, 4, 8, 8])
        self.assertEqual(str(module), 'ℤ^5 ⊕ ℤ/2ℤ ⊕ ℤ/2ℤ ⊕ ℤ/4ℤ ⊕ ℤ/8ℤ ⊕ ℤ/8ℤ')


if __name__ == '__main__':
    unittest.main()

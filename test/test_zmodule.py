import unittest
from homology.zmodule import FinitelyGeneratedZModule


class TestZModule(unittest.TestCase):
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

    def test_zero_module(self):
        module = FinitelyGeneratedZModule.zero()
        self.assertEqual(module.rank, 0)
        self.assertEqual(module.torsion_numbers, [])

    def test_free_module(self):
        module = FinitelyGeneratedZModule.free(37)
        self.assertEqual(module.rank, 37)
        self.assertEqual(module.torsion_numbers, [])

    def test_printing_element_0(self):
        module = FinitelyGeneratedZModule.zero()
        element = module.element([1])
        self.assertEqual(str(element), "0")

    def test_printing_element_cyclic_free(self):
        module = FinitelyGeneratedZModule.free(1)
        element = module.element([-1])
        self.assertEqual(str(element), "-1")

    def test_printing_element_cyclic_quotient(self):
        module = FinitelyGeneratedZModule(0, [3])
        element = module.element([-1])
        self.assertEqual(str(element), "2 + 3ℤ")

    def test_printing_element_free(self):
        module = FinitelyGeneratedZModule.free(2)
        element = module.element([1, 2])
        self.assertEqual(str(element), "(1, 2)")

    def test_printing_element_mixed(self):
        module = FinitelyGeneratedZModule(2, [3, 6])
        element = module.element([1, 2, 2, 4])
        self.assertEqual(str(element), "(1, 2, 2 + 3ℤ, 4 + 6ℤ)")

    def test_printing_element_normalization(self):
        module = FinitelyGeneratedZModule(2, [3, 6])
        element = module.element([1, 2, 3, -4])
        self.assertEqual(str(element), "(1, 2, 0 + 3ℤ, 2 + 6ℤ)")


if __name__ == '__main__':
    unittest.main()

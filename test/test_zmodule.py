import unittest
from module_theory.zmodule import ZModule


class TestZModule(unittest.TestCase):
    def test_printing_0(self):
        module = ZModule(0, [])
        self.assertEqual(str(module), '0')

    def test_printing_Z(self):
        module = ZModule(1, [])
        self.assertEqual(str(module), 'ℤ')

    def test_printing_Z_with_rank(self):
        module = ZModule(5, [])
        self.assertEqual(str(module), 'ℤ^5')

    def test_printing_cyclic(self):
        module = ZModule(0, [2])
        self.assertEqual(str(module), 'ℤ/2ℤ')

    def test_printing_torsion(self):
        module = ZModule(0, [2, 4])
        self.assertEqual(str(module), 'ℤ/2ℤ ⊕ ℤ/4ℤ')

    def test_printing_all(self):
        module = ZModule(5, [2, 2, 4, 8, 8])
        self.assertEqual(str(module),
                         'ℤ^5 ⊕ ℤ/2ℤ ⊕ ℤ/2ℤ ⊕ ℤ/4ℤ ⊕ ℤ/8ℤ ⊕ ℤ/8ℤ')

    def test_zero_module(self):
        module = ZModule.zero()
        self.assertEqual(module.rank, 0)
        self.assertEqual(module.torsion_numbers, ())

    def test_free_module(self):
        module = ZModule.free(37)
        self.assertEqual(module.rank, 37)
        self.assertEqual(module.torsion_numbers, ())

    def test_printing_element_0(self):
        module = ZModule.zero()
        element = module.element([1])
        self.assertEqual(str(element), "0")

    def test_printing_element_cyclic_free(self):
        module = ZModule.free(1)
        element = module.element([-1])
        self.assertEqual(str(element), "-1")

    def test_printing_element_cyclic_quotient(self):
        module = ZModule(0, [3])
        element = module.element([-1])
        self.assertEqual(str(element), "2 + 3ℤ")

    def test_printing_element_free(self):
        module = ZModule.free(2)
        element = module.element([1, 2])
        self.assertEqual(str(element), "(1, 2)")

    def test_printing_element_mixed(self):
        module = ZModule(2, [3, 6])
        element = module.element([1, 2, 2, 4])
        self.assertEqual(str(element), "(1, 2, 2 + 3ℤ, 4 + 6ℤ)")

    def test_printing_element_normalization(self):
        module = ZModule(2, [3, 6])
        element = module.element([1, 2, 3, -4])
        self.assertEqual(str(element), "(1, 2, 0 + 3ℤ, 2 + 6ℤ)")

    def test_addition(self):
        module = ZModule(2, [3, 6])
        element1 = module.element([1, 2, 2, 4])
        element2 = module.element([-1, -2, -2, -4])
        sum_of_elements = element1 + element2
        self.assertEqual(sum_of_elements.coordinates, (0, 0, 0, 0))

    def test_sum_of_list(self):
        module = ZModule(2, [3, 6])
        list_of_elements = [
            module.element([1, 0, 0, 0]),
            module.element([0, 1, 0, 0]),
            module.element([0, 0, 1, 0]),
            module.element([0, 0, 0, 1])
        ]
        sum_of_list = sum(list_of_elements)
        self.assertEqual(sum_of_list.coordinates, (1, 1, 1, 1))

    def test_canonical_coordinates_zero(self):
        module = ZModule.zero()
        generators = module.canonical_generators()
        self.assertEqual(len(generators), 1)
        self.assertEqual(generators[0].coordinates, (0,))

    def test_canonical_coordinates_Z(self):
        module = ZModule(1, [])
        generators = module.canonical_generators()
        self.assertEqual(len(generators), 1)
        self.assertEqual(generators[0].coordinates, (1,))

    def test_canonical_coordinates_cyclic_torsion(self):
        module = ZModule(0, [2])
        generators = module.canonical_generators()
        self.assertEqual(len(generators), 1)
        self.assertEqual(generators[0].coordinates, (1,))

    def test_canonical_coordinates(self):
        module = ZModule(2, [3, 3, 18])
        generators = module.canonical_generators()
        self.assertEqual(len(generators), 5)
        self.assertEqual(generators[0].coordinates, (1, 0, 0, 0, 0))
        self.assertEqual(generators[1].coordinates, (0, 1, 0, 0, 0))
        self.assertEqual(generators[2].coordinates, (0, 0, 1, 0, 0))
        self.assertEqual(generators[3].coordinates, (0, 0, 0, 1, 0))
        self.assertEqual(generators[4].coordinates, (0, 0, 0, 0, 1))


if __name__ == '__main__':
    unittest.main()

import unittest
from module_theory.zmodule import ZModule
from module_theory.operators.submodule_quotient import SubmoduleQuotient


class TestSubmoduleQuotient(unittest.TestCase):
    def test_sumbodule_quotient(self):
        module = ZModule.free(3)
        generators = module.canonical_generators()
        kernel_generators = [
            module.element([3, 0, 2]),
            module.element([2, 2, 2]),
            module.element([3, 0, 2])
        ]
        quotient = SubmoduleQuotient(generators, kernel_generators)
        self.assertEqual(quotient.rank, 1)
        self.assertEqual(quotient.torsion_numbers, (2,))


if __name__ == '__main__':
    unittest.main()

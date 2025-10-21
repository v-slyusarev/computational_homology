import unittest
from module_theory.zmodule import ZModule
from module_theory.operators.submodule_quotient import (
    SubmoduleQuotient, Submodule, Quotient
)


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

    def test_sumbodule_trivial(self):
        module = ZModule.free(3)
        submodule = Submodule([])
        self.assertTrue(submodule.is_zero())

    def test_sumbodule_zero(self):
        module = ZModule.free(3)
        submodule = Submodule([module.zero_element()] * 5)
        self.assertTrue(submodule.is_zero())

    def test_sumbodule_independent(self):
        module = ZModule.free(3)
        submodule = Submodule([
            module.element([-1, 0, 3]), module.element([2, 2, 2])
        ])
        self.assertTrue(submodule.is_identical_to(ZModule.free(2)))

    def test_sumbodule_dependent(self):
        module = ZModule.free(3)
        submodule = Submodule([
            module.element([-1, 0, 3]), module.element([2, 0, -6])
        ])
        self.assertTrue(submodule.is_identical_to(ZModule.free(1)))

    def test_quotient_trivial(self):
        module = ZModule.free(3)
        quotient = Quotient(module, [])
        self.assertTrue(quotient.is_identical_to(module))

    def test_quotient_by_zero(self):
        module = ZModule.free(3)
        quotient = Quotient(module, [module.zero_element()])
        self.assertTrue(quotient.is_identical_to(module))

    def test_quotient_by_self(self):
        module = ZModule.free(3)
        quotient = Quotient(module, module.canonical_generators())
        self.assertTrue(quotient.is_zero())

    def test_quotient_free(self):
        module = ZModule.free(3)
        quotient = Quotient(module, [module.element([1, 1, 1])])
        self.assertTrue(quotient.is_identical_to(ZModule.free(2)))

    def test_quotient_with_torsion(self):
        module = ZModule.free(3)
        quotient = Quotient(module, [module.element([2, 4, 6])])
        print(quotient)
        self.assertTrue(quotient.is_identical_to(ZModule(2, [2])))


if __name__ == '__main__':
    unittest.main()

import unittest
from module_theory.zmodule import ZModule
from module_theory.cyclic_zmodule import FreeCyclicZModule, TorsionCyclicZModule
from module_theory.operators.cyclic_summands import cyclic_summands


class TestCyclicSummands(unittest.TestCase):
    def test_zero_module(self):
        module = ZModule.zero()
        summands = cyclic_summands(module)
        self.assertEqual(len(summands), 1)
        self.assertIsInstance(summands[0], ZModule)
        self.assertTrue(summands[0].is_zero)

    def test_cyclic_summands(self):
        module = ZModule(3, [2, 4, 100])
        summands = cyclic_summands(module)
        self.assertEqual(len(summands), 6)
        self.assertIsInstance(summands[0], FreeCyclicZModule)
        self.assertIsInstance(summands[1], FreeCyclicZModule)
        self.assertIsInstance(summands[2], FreeCyclicZModule)
        self.assertIsInstance(summands[3], TorsionCyclicZModule)
        self.assertIsInstance(summands[4], TorsionCyclicZModule)
        self.assertIsInstance(summands[5], TorsionCyclicZModule)
        self.assertEqual(summands[3].torsion, 2)
        self.assertEqual(summands[4].torsion, 4)
        self.assertEqual(summands[5].torsion, 100)


if __name__ == '__main__':
    unittest.main()

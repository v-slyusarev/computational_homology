import unittest
from module_theory.zmodule import ZModule
from module_theory.cyclic_zmodule import FreeCyclicZModule, TorsionCyclicZModule


class TestCyclicZModule(unittest.TestCase):
    def test_free_cyclic_z_module(self):
        Z = FreeCyclicZModule()
        self.assertIsInstance(Z, ZModule)
        self.assertEqual(Z.rank, 1)
        self.assertEqual(Z.torsion_numbers, [])
        self.assertEqual(Z.dimensions(), 1)
        self.assertEqual(Z.zero_element().coordinates, [0])

    def test_torsion_cyclic_z_module(self):
        Z100 = TorsionCyclicZModule(100)
        self.assertIsInstance(Z100, ZModule)
        self.assertEqual(Z100.rank, 0)
        self.assertEqual(Z100.torsion_numbers, [100])
        self.assertEqual(Z100.torsion, 100)
        self.assertEqual(Z100.dimensions(), 1)
        self.assertEqual(Z100.zero_element().coordinates, [0])


if __name__ == '__main__':
    unittest.main()

import unittest
from module_theory.zmodule import ZModule
from module_theory.homomorphism import Homomorphism
from module_theory.cochain_complex import CochainComplex
from module_theory.homology import homology


class TestHomology(unittest.TestCase):
    def test_homology(self):
        Z3 = ZModule.free(3)
        cochain_complex = CochainComplex(
            modules=[Z3, Z3],
            homomorphisms=[Homomorphism([
                [3, 2, 3],
                [0, 2, 0],
                [2, 2, 2]
            ], Z3, Z3)]
        )
        H = homology(cochain_complex)
        self.assertEqual(len(H), 2)
        self.assertTrue(H[0].is_identical_to(ZModule.free(1)))
        self.assertTrue(H[1].is_identical_to(ZModule(1, [2])))


if __name__ == '__main__':
    unittest.main()

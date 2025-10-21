import unittest
from module_theory.zmodule import ZModule
from module_theory.cyclic_zmodule import (
    FreeCyclicZModule, TorsionCyclicZModule
)
from module_theory.homomorphism import Homomorphism
from module_theory.cochain_complex import CochainComplex
from module_theory.cohomology import cohomology


class TestCohomology(unittest.TestCase):
    def test_two_exact(self):
        Z = FreeCyclicZModule()
        cochain_complex = CochainComplex(
            modules=[Z, Z],
            homomorphisms=[Homomorphism([
                [2]
            ], Z, Z)]
        )
        H = cohomology(cochain_complex)
        self.assertEqual(len(H), 2)
        self.assertTrue(H[0].is_zero())
        self.assertTrue(H[1].is_identical_to(TorsionCyclicZModule(2)))

    def test_two(self):
        Zsquare = ZModule.free(2)
        cochain_complex = CochainComplex(
            modules=[Zsquare, Zsquare],
            homomorphisms=[Homomorphism([
                [1, 2],
                [0, 2]
            ], Zsquare, Zsquare)]
        )
        H = cohomology(cochain_complex)
        self.assertEqual(len(H), 2)
        self.assertTrue(H[0].is_zero())
        self.assertTrue(H[1].is_identical_to(TorsionCyclicZModule(2)))

    def test_exact(self):
        Z = ZModule.free(1)
        Zsquare = ZModule.free(2)
        Zcube = ZModule.free(3)
        cochain_complex = CochainComplex(
            modules=[Zsquare, Zcube, Z],
            homomorphisms=[
                Homomorphism([
                    [1, 0],
                    [0, 1],
                    [0, 0]
                ], Zsquare, Zcube),
                Homomorphism([
                    [0, 0, 1],
                ], Zcube, Z),
            ]
        )
        H = cohomology(cochain_complex)
        self.assertEqual(len(H), 3)
        self.assertTrue(H[0].is_zero())
        self.assertTrue(H[1].is_zero())
        self.assertTrue(H[2].is_zero())

    def test_nonexact(self):
        Z = ZModule.free(1)
        Zsquare = ZModule.free(2)
        cochain_complex = CochainComplex(
            modules=[Z, Zsquare, Z],
            homomorphisms=[
                Homomorphism([
                    [2],
                    [0],
                ], Z, Zsquare),
                Homomorphism([
                    [0, 1],
                ], Zsquare, Z),
            ]
        )
        H = cohomology(cochain_complex)
        self.assertEqual(len(H), 3)
        self.assertTrue(H[0].is_zero())
        self.assertTrue(H[1].is_identical_to(TorsionCyclicZModule(2)))
        self.assertTrue(H[2].is_zero())

    def test_nonzero_kernel(self):
        Zsquare = ZModule.free(2)
        cochain_complex = CochainComplex(
            modules=[Zsquare, Zsquare],
            homomorphisms=[
                Homomorphism([
                    [-2, 2],
                    [0, 0],
                ], Zsquare, Zsquare),
            ]
        )
        H = cohomology(cochain_complex)
        self.assertEqual(len(H), 2)
        self.assertTrue(H[0].is_identical_to(FreeCyclicZModule()))
        self.assertTrue(H[1].is_identical_to(ZModule(1, [2])))
        # self.assertTrue(H[2].is_zero())


if __name__ == '__main__':
    unittest.main()

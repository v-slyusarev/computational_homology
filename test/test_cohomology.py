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

    def test_torsion_in_domain(self):
        C0 = ZModule(1, [4])
        C1 = ZModule(1, [2])
        d1 = Homomorphism((
            (2, 0),
            (0, 1)
        ), C0, C1)
        cochain_complex = CochainComplex(
            modules=[C0, C1],
            homomorphisms=[d1]
        )
        H = cohomology(cochain_complex)
        self.assertEqual(len(H), 2)
        self.assertTrue(H[0].is_identical_to(TorsionCyclicZModule(2)))
        self.assertTrue(H[1].is_identical_to(TorsionCyclicZModule(2)))

    def test_short_exact_sequence_torsion(self):
        C0 = ZModule(1, [2])
        C1 = ZModule(2, [2, 4])
        C2 = ZModule(1, [4])
        d1 = Homomorphism((
            (1, 0),
            (0, 0),
            (0, 1),
            (0, 0)
        ), C0, C1)
        d2 = Homomorphism((
            (0, 1, 0, 0),
            (0, 0, 0, 1)
        ), C1, C2)
        cochain_complex = CochainComplex(
            modules=[C0, C1, C2],
            homomorphisms=[d1, d2]
        )
        H = cohomology(cochain_complex)
        self.assertEqual(len(H), 3)
        self.assertTrue(H[0].is_zero())
        self.assertTrue(H[1].is_zero())
        self.assertTrue(H[2].is_zero())

    def test_non_exact_torsion(self):
        C0 = ZModule(1, [2])
        C1 = ZModule(2, [2, 4])
        C2 = ZModule(1, [4])
        d1 = Homomorphism((
            (2, 0),
            (0, 0),
            (0, 1),
            (0, 0)
        ), C0, C1)
        d2 = Homomorphism((
            (0, 1, 0, 0),
            (0, 0, 0, 1)
        ), C1, C2)
        cochain_complex = CochainComplex(
            modules=[C0, C1, C2],
            homomorphisms=[d1, d2]
        )
        H = cohomology(cochain_complex)
        self.assertEqual(len(H), 3)
        self.assertTrue(H[0].is_zero())
        self.assertTrue(H[1].is_identical_to(TorsionCyclicZModule(2)))
        self.assertTrue(H[2].is_zero())

    def test_torsion_two(self):
        Z20 = TorsionCyclicZModule(20)
        d1 = Homomorphism(((4,),), Z20, Z20)
        d2 = Homomorphism(((10,),), Z20, Z20)
        cochain_complex = CochainComplex(
            modules=[Z20, Z20, Z20],
            homomorphisms=[d1, d2]
        )
        H = cohomology(cochain_complex)
        self.assertEqual(len(H), 3)
        self.assertTrue(H[0].is_identical_to(TorsionCyclicZModule(4)))
        self.assertTrue(H[1].is_identical_to(TorsionCyclicZModule(2)))
        self.assertTrue(H[2].is_identical_to(TorsionCyclicZModule(10)))

    def test_torsion_three(self):
        C0 = ZModule(0, [4, 6])
        C1 = ZModule(0, [2, 6])
        C2 = ZModule(0, [6])
        d1 = Homomorphism((
            (1, 1),
            (0, 2),
        ), C0, C1)
        d2 = Homomorphism(((0, 3),), C1, C2)
        cochain_complex = CochainComplex(
            modules=[C0, C1, C2],
            homomorphisms=[d1, d2]
        )
        H = cohomology(cochain_complex)
        self.assertEqual(len(H), 3)
        self.assertTrue(H[0].is_identical_to(TorsionCyclicZModule(4)))
        self.assertTrue(H[1].is_zero())
        self.assertTrue(H[2].is_identical_to(TorsionCyclicZModule(3)))

    def test_mixed_three(self):
        C0 = ZModule(1, [4])
        C1 = ZModule(2, [2])
        C2 = ZModule(1, [4])
        d1 = Homomorphism((
            (1, 0),
            (2, 0),
            (1, 1),
        ), C0, C1)
        d2 = Homomorphism((
            (-2, 1, 0),
            (0, 0, 0),
        ), C1, C2)
        cochain_complex = CochainComplex(
            modules=[C0, C1, C2],
            homomorphisms=[d1, d2]
        )
        H = cohomology(cochain_complex)
        self.assertEqual(len(H), 3)
        self.assertTrue(H[0].is_identical_to(TorsionCyclicZModule(2)))
        self.assertTrue(H[1].is_zero())
        self.assertTrue(H[2].is_identical_to(TorsionCyclicZModule(4)))


if __name__ == '__main__':
    unittest.main()

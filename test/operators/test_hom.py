import unittest
from homology.zmodule import FinitelyGeneratedZModule
from homology.homomorphism import Homomorphism
from homology.operators.hom import hom


class TestHom(unittest.TestCase):
    def test_hom_from_0(self):
        A = FinitelyGeneratedZModule.zero()
        B = FinitelyGeneratedZModule(3, [2, 4, 6])
        homAB, _, _ = hom(A, B)
        self.assertEqual(homAB.rank, 0)
        self.assertEqual(homAB.torsion_numbers, [])

    def test_hom_to_0(self):
        A = FinitelyGeneratedZModule(3, [2, 4, 6])
        B = FinitelyGeneratedZModule.zero()
        homAB, _, _ = hom(A, B)
        self.assertEqual(homAB.rank, 0)
        self.assertEqual(homAB.torsion_numbers, [])

    def test_hom_free_to_free(self):
        A = FinitelyGeneratedZModule(3, [])
        B = FinitelyGeneratedZModule(7, [])
        homAB, _, _ = hom(A, B)
        self.assertEqual(homAB.rank, 21)
        self.assertEqual(homAB.torsion_numbers, [])

    def test_hom_free_to_torsion(self):
        A = FinitelyGeneratedZModule(3, [])
        B = FinitelyGeneratedZModule(0, [2])
        homAB, _, _ = hom(A, B)
        self.assertEqual(homAB.rank, 0)
        self.assertEqual(homAB.torsion_numbers, [2, 2, 2])

    def test_hom_torsion_to_free(self):
        A = FinitelyGeneratedZModule(0, [3])
        B = FinitelyGeneratedZModule(2, [])
        homAB, _, _ = hom(A, B)
        self.assertEqual(homAB.rank, 0)
        self.assertEqual(homAB.torsion_numbers, [])

    def test_hom_torsion_to_torsion(self):
        A = FinitelyGeneratedZModule(0, [10])
        B = FinitelyGeneratedZModule(0, [15])
        homAB, _, _ = hom(A, B)
        self.assertEqual(homAB.rank, 0)
        self.assertEqual(homAB.torsion_numbers, [5])


if __name__ == '__main__':
    unittest.main()

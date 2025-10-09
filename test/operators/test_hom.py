import unittest
from homology.zmodule import ZModule
from homology.homomorphism import Homomorphism
from homology.chain_complex import ChainComplex
from homology.operators.hom import hom, left_hom


class TestHom(unittest.TestCase):
    def test_hom_from_0(self):
        A = ZModule.zero()
        B = ZModule(3, [2, 4, 6])
        homAB, _, _ = hom(A, B)
        self.assertEqual(homAB.rank, 0)
        self.assertEqual(homAB.torsion_numbers, [])

    def test_hom_to_0(self):
        A = ZModule(3, [2, 4, 6])
        B = ZModule.zero()
        homAB, _, _ = hom(A, B)
        self.assertEqual(homAB.rank, 0)
        self.assertEqual(homAB.torsion_numbers, [])

    def test_hom_free_to_free(self):
        A = ZModule(3, [])
        B = ZModule(7, [])
        homAB, _, _ = hom(A, B)
        self.assertEqual(homAB.rank, 21)
        self.assertEqual(homAB.torsion_numbers, [])

    def test_hom_free_to_torsion(self):
        A = ZModule(3, [])
        B = ZModule(0, [2])
        homAB, _, _ = hom(A, B)
        self.assertEqual(homAB.rank, 0)
        self.assertEqual(homAB.torsion_numbers, [2, 2, 2])

    def test_hom_torsion_to_free(self):
        A = ZModule(0, [3])
        B = ZModule(2, [])
        homAB, _, _ = hom(A, B)
        self.assertEqual(homAB.rank, 0)
        self.assertEqual(homAB.torsion_numbers, [])

    def test_hom_torsion_to_torsion(self):
        A = ZModule(0, [10])
        B = ZModule(0, [15])
        homAB, _, _ = hom(A, B)
        self.assertEqual(homAB.rank, 0)
        self.assertEqual(homAB.torsion_numbers, [5])

    def test_conversions(self):
        A = ZModule(1, [2, 4])
        B = ZModule(2, [5, 10])
        homAB, matrix_to_hom, hom_to_matrix = hom(A, B)
        self.assertEqual(homAB.rank, 2)
        self.assertEqual(homAB.torsion_numbers, [5, 10, 2, 2])
        matrix = [
            [1, 0, 0],
            [2, 0, 0],
            [3, 0, 0],
            [4, 1, 1],
        ]
        hom_element = matrix_to_hom(matrix)
        self.assertEqual(hom_element.coordinates, [1, 2, 3, 4, 1, 1])
        restored_matrix = hom_to_matrix(hom_element)
        self.assertEqual(restored_matrix, matrix)

    def test_left_hom_Z_to_Z(self):
        Z = ZModule.free(1)
        chain_complex = ChainComplex([Z, Z], [Homomorphism([[2]], Z, Z)])
        hom_chain_complex = left_hom(chain_complex, Z)
        # print(hom_chain_complex)
        # print(hom_chain_complex.homomorphisms[0].matrix)
        self.assertEqual(len(hom_chain_complex.modules), 2)
        self.assertEqual(hom_chain_complex.modules[0].rank, 1)
        self.assertEqual(hom_chain_complex.modules[0].torsion_numbers, [])
        self.assertEqual(hom_chain_complex.modules[1].rank, 1)
        self.assertEqual(hom_chain_complex.modules[1].torsion_numbers, [])
        self.assertEqual(len(hom_chain_complex.homomorphisms), 2)
        self.assertEqual(hom_chain_complex.homomorphisms[0].matrix, [[2]])
        self.assertEqual(hom_chain_complex.homomorphisms[1].matrix, [[0]])


if __name__ == '__main__':
    unittest.main()

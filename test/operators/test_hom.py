import unittest
from module_theory.zmodule import ZModule
from module_theory.cyclic_zmodule import FreeCyclicZModule, TorsionCyclicZModule
from module_theory.homomorphism import Homomorphism
from module_theory.chain_complex import ChainComplex
from module_theory.operators.direct_sum import direct_sum
from module_theory.operators.hom import Hom, left_hom, right_hom


class TestHom(unittest.TestCase):
    def test_hom_from_0(self):
        A = ZModule.zero()
        B = ZModule(3, [2, 4, 6])
        homAB = Hom(A, B)
        self.assertEqual(homAB.rank, 0)
        self.assertEqual(homAB.torsion_numbers, [])

    def test_hom_to_0(self):
        A = ZModule(3, [2, 4, 6])
        B = ZModule.zero()
        homAB = Hom(A, B)
        self.assertEqual(homAB.rank, 0)
        self.assertEqual(homAB.torsion_numbers, [])

    def test_hom_free_to_free(self):
        A = ZModule(3, [])
        B = ZModule(7, [])
        homAB = Hom(A, B)
        self.assertEqual(homAB.rank, 21)
        self.assertEqual(homAB.torsion_numbers, [])

    def test_hom_free_to_torsion(self):
        A = ZModule(3, [])
        B = ZModule(0, [2])
        homAB = Hom(A, B)
        self.assertEqual(homAB.rank, 0)
        self.assertEqual(homAB.torsion_numbers, [2, 2, 2])

    def test_hom_torsion_to_free(self):
        A = ZModule(0, [3])
        B = ZModule(2, [])
        homAB = Hom(A, B)
        self.assertEqual(homAB.rank, 0)
        self.assertEqual(homAB.torsion_numbers, [])

    def test_hom_torsion_to_torsion(self):
        A = ZModule(0, [10])
        B = ZModule(0, [15])
        homAB = Hom(A, B)
        self.assertEqual(homAB.rank, 0)
        self.assertEqual(homAB.torsion_numbers, [5])

    def test_conversions(self):
        A = ZModule(1, [2, 4])
        B = ZModule(2, [5, 10])
        homAB = Hom(A, B)
        self.assertEqual(homAB.rank, 2)
        self.assertEqual(homAB.torsion_numbers, [5, 10, 2, 2])
        matrix = [[1, 0, 0],
                  [2, 0, 0],
                  [3, 0, 0],
                  [4, 1, 1]]
        homomorphism = Homomorphism(matrix, A, B)
        hom_element = homAB.element_from_homomorphism(homomorphism)
        self.assertEqual(hom_element.coordinates, [1, 2, 3, 4, 1, 1])
        restored_homomorphism = homAB.homomorphism_from_element(hom_element)
        self.assertEqual(restored_homomorphism.matrix, matrix)

    def test_left_hom_Z_to_Z(self):
        Z = ZModule.free(1)
        chain_complex = ChainComplex([Z, Z], [Homomorphism([[2]], Z, Z)])
        hom_chain_complex = left_hom(chain_complex, Z)
        self.assertEqual(len(hom_chain_complex.modules), 2)
        self.assertEqual(hom_chain_complex.modules[0].rank, 1)
        self.assertEqual(hom_chain_complex.modules[0].torsion_numbers, [])
        self.assertEqual(hom_chain_complex.modules[1].rank, 1)
        self.assertEqual(hom_chain_complex.modules[1].torsion_numbers, [])
        self.assertEqual(len(hom_chain_complex.homomorphisms), 2)
        self.assertEqual(hom_chain_complex.homomorphisms[0].matrix, [[2]])
        self.assertEqual(hom_chain_complex.homomorphisms[1].matrix, [[0]])

    def test_left_hom_torsion_to_free(self):
        A = ZModule.free(4)
        chain_complex = ChainComplex(
            modules=[A] * 3,
            homomorphisms=[Homomorphism.identity(A)] * 2
        )
        hom_chain_complex = left_hom(chain_complex, ZModule(0, [2, 4, 8]))
        self.assertEqual(len(hom_chain_complex.modules), 3)
        self.assertTrue(hom_chain_complex.modules[0].is_zero())
        self.assertTrue(hom_chain_complex.modules[1].is_zero())
        self.assertTrue(hom_chain_complex.modules[2].is_zero())
        self.assertEqual(len(hom_chain_complex.homomorphisms), 3)
        self.assertTrue(hom_chain_complex.homomorphisms[0].is_zero())
        self.assertTrue(hom_chain_complex.homomorphisms[1].is_zero())
        self.assertTrue(hom_chain_complex.homomorphisms[2].is_zero())

    def test_left_hom_splitting(self):
        A = TorsionCyclicZModule(3)
        C = TorsionCyclicZModule(6)
        B, embeddings = direct_sum(A, C)

        chain_complex = ChainComplex(
            modules=[A, B, C],
            homomorphisms=[
                embeddings[0],
                Homomorphism(
                    matrix=[[0, 1]],
                    domain=B,
                    codomain=C)
            ]
        )

        D = ZModule.free(2)
        hom_chain_complex = left_hom(chain_complex, D)

        self.assertEqual(len(hom_chain_complex.modules), 3)
        self.assertEqual(hom_chain_complex.modules[0].rank, 0)
        self.assertEqual(hom_chain_complex.modules[0].torsion_numbers, [3, 3])
        self.assertEqual(hom_chain_complex.modules[1].rank, 0)
        self.assertEqual(
            hom_chain_complex.modules[1].torsion_numbers, [3, 3, 6, 6]
        )
        self.assertEqual(hom_chain_complex.modules[2].rank, 0)
        self.assertEqual(hom_chain_complex.modules[2].torsion_numbers, [6, 6])
        self.assertEqual(len(hom_chain_complex.homomorphisms), 3)
        self.assertEqual(
            hom_chain_complex.homomorphisms[0].matrix,
            [[1, 0],
             [0, 1],
             [0, 0],
             [0, 0]]
        )
        self.assertEqual(
            hom_chain_complex.homomorphisms[1].matrix,
            [[0, 0, 1, 0],
             [0, 0, 0, 1]]
        )
        self.assertTrue(hom_chain_complex.homomorphisms[2].is_zero())

    def test_right_hom_to_torsion(self):
        A = FreeCyclicZModule()
        B = TorsionCyclicZModule(5)
        D = TorsionCyclicZModule(10)
        chain_complex = ChainComplex([A, B], [Homomorphism([[2]], A, B)])
        hom_chain_complex = right_hom(chain_complex, D)
        self.assertEqual(len(hom_chain_complex.modules), 2)
        self.assertEqual(hom_chain_complex.modules[0].rank, 0)
        self.assertEqual(hom_chain_complex.modules[0].torsion_numbers, [5])
        self.assertEqual(hom_chain_complex.modules[1].rank, 0)
        self.assertEqual(hom_chain_complex.modules[1].torsion_numbers, [10])
        self.assertEqual(len(hom_chain_complex.homomorphisms), 2)
        self.assertEqual(hom_chain_complex.homomorphisms[0].matrix, [[2]])
        self.assertEqual(hom_chain_complex.homomorphisms[1].matrix, [[0]])

    def test_right_hom_splitting(self):
        A = ZModule.free(2)
        C = FreeCyclicZModule()
        B, embeddings = direct_sum(A, C)

        chain_complex = ChainComplex(
            modules=[A, B, C],
            homomorphisms=[
                embeddings[0],
                Homomorphism(
                    matrix=[[0, 0, 1]],
                    domain=B,
                    codomain=C)
            ]
        )

        D = TorsionCyclicZModule(2)
        hom_chain_complex = right_hom(chain_complex, D)

        self.assertEqual(len(hom_chain_complex.modules), 3)
        self.assertEqual(hom_chain_complex.modules[0].rank, 0)
        self.assertEqual(hom_chain_complex.modules[0].torsion_numbers, [2])
        self.assertEqual(hom_chain_complex.modules[1].rank, 0)
        self.assertEqual(
            hom_chain_complex.modules[1].torsion_numbers, [2, 2, 2]
        )
        self.assertEqual(hom_chain_complex.modules[2].rank, 0)
        self.assertEqual(hom_chain_complex.modules[2].torsion_numbers, [2, 2])
        self.assertEqual(len(hom_chain_complex.homomorphisms), 3)
        self.assertEqual(
            hom_chain_complex.homomorphisms[0].matrix,
            [[0],
             [0],
             [1]]
        )
        self.assertEqual(
            hom_chain_complex.homomorphisms[1].matrix,
            [[1, 0, 0],
             [0, 1, 0]]
        )
        self.assertTrue(hom_chain_complex.homomorphisms[2].is_zero())


if __name__ == '__main__':
    unittest.main()

import unittest
from homology.zmodule import FinitelyGeneratedZModule
from homology.homomorphism import Homomorphism
from homology.operators.direct_sum import direct_sum


class TestDirectSum(unittest.TestCase):
    def test_empty_sum(self):
        module, embeddings = direct_sum([])
        self.assertEqual(module.rank, 0)
        self.assertEqual(module.torsion_numbers, [])
        self.assertEqual(embeddings, [])

    def test_sum_with_zero(self):
        module = FinitelyGeneratedZModule(3, [2, 4, 8])
        sum_module, embeddings = direct_sum([
            FinitelyGeneratedZModule.zero(),
            module,
            FinitelyGeneratedZModule.zero()
        ])

        self.assertEqual(sum_module.rank, 3)
        self.assertEqual(sum_module.torsion_numbers, [2, 4, 8])
        self.assertEqual(embeddings[0].matrix, [[0] for _ in range(6)])
        self.assertEqual(embeddings[1].matrix,
                         Homomorphism.identity(module).matrix)
        self.assertEqual(embeddings[2].matrix, [[0] for _ in range(6)])

    def test_sum_with_zero_inside(self):
        A = FinitelyGeneratedZModule(1, [2])
        B = FinitelyGeneratedZModule(2, [])
        sum_module, embeddings = direct_sum([
            A,
            FinitelyGeneratedZModule.zero(),
            B
        ])

        self.assertEqual(sum_module.rank, 3)
        self.assertEqual(sum_module.torsion_numbers, [2])
        self.assertEqual(
            embeddings[0].matrix,
            [[1, 0],
             [0, 0],
             [0, 0],
             [0, 1]]
        )
        self.assertEqual(embeddings[1].matrix, [[0] for _ in range(4)])
        self.assertEqual(
            embeddings[2].matrix,
            [[0, 0],
             [1, 0],
             [0, 1],
             [0, 0]])

    def test_sum_three(self):
        A = FinitelyGeneratedZModule(0, [2])
        B = FinitelyGeneratedZModule(2, [])
        C = FinitelyGeneratedZModule(1, [2, 3])
        sum_module, embeddings = direct_sum([
            A,
            B,
            C
        ])

        self.assertEqual(sum_module.rank, 3)
        self.assertEqual(sum_module.torsion_numbers, [2, 2, 3])
        self.assertEqual(
            embeddings[0].matrix,
            [[0],
             [0],
             [0],
             [1],
             [0],
             [0]]
        )
        self.assertEqual(embeddings[1].matrix,
            [[1, 0],
             [0, 1],
             [0, 0],
             [0, 0],
             [0, 0],
             [0, 0]]
        )
        self.assertEqual(
            embeddings[2].matrix,
            [[0, 0, 0],
             [0, 0, 0],
             [1, 0, 0],
             [0, 0, 0],
             [0, 1, 0],
             [0, 0, 1]]
         )


if __name__ == '__main__':
    unittest.main()

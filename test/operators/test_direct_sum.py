import unittest
from module_theory.zmodule import ZModule
from module_theory.homomorphism import Homomorphism
from module_theory.operators.direct_sum import direct_sum


class TestDirectSum(unittest.TestCase):
    def test_empty_sum(self):
        module, embeddings = direct_sum()
        self.assertEqual(module.rank, 0)
        self.assertEqual(module.torsion_numbers, [])
        self.assertEqual(embeddings, [])

    def test_sum_with_zero(self):
        module = ZModule(3, [2, 4, 8])
        sum_module, embeddings = direct_sum(
            ZModule.zero(),
            module,
            ZModule.zero()
        )

        self.assertEqual(sum_module.rank, 3)
        self.assertEqual(sum_module.torsion_numbers, [2, 4, 8])
        self.assertEqual(embeddings[0].matrix, [[0] for _ in range(6)])
        self.assertEqual(embeddings[1].matrix,
                         Homomorphism.identity(module).matrix)
        self.assertEqual(embeddings[2].matrix, [[0] for _ in range(6)])

    def test_sum_with_zero_inside(self):
        A = ZModule(1, [2])
        B = ZModule(2, [])
        sum_module, embeddings = direct_sum(A, ZModule.zero(), B)

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
        A = ZModule(0, [2])
        B = ZModule(2, [])
        C = ZModule(1, [2, 3])
        sum_module, embeddings = direct_sum(A, B, C)

        self.assertEqual(sum_module.rank, 3)
        self.assertEqual(sum_module.torsion_numbers, [2, 2, 3])
        self.assertEqual(embeddings[0].matrix, [[0],
                                                [0],
                                                [0],
                                                [1],
                                                [0],
                                                [0]])

        self.assertEqual(embeddings[1].matrix, [[1, 0],
                                                [0, 1],
                                                [0, 0],
                                                [0, 0],
                                                [0, 0],
                                                [0, 0]])

        self.assertEqual(embeddings[2].matrix, [[0, 0, 0],
                                                [0, 0, 0],
                                                [1, 0, 0],
                                                [0, 0, 0],
                                                [0, 1, 0],
                                                [0, 0, 1]])


if __name__ == '__main__':
    unittest.main()

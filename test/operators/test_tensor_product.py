import unittest
from module_theory.zmodule import ZModule
from module_theory.homomorphism import Homomorphism
from module_theory.cyclic_zmodule import FreeCyclicZModule, TorsionCyclicZModule
from module_theory.operators.tensor_product import TensorProduct


class TestTensorProduct(unittest.TestCase):
    def test_tensor_product_with_zero(self):
        tensor_product = TensorProduct(
            ZModule.zero(), FreeCyclicZModule(), TorsionCyclicZModule(10)
        )
        self.assertTrue(tensor_product.is_zero())

    def test_tensor_product_of_free(self):
        tensor_product = TensorProduct(
            ZModule.free(1),
            ZModule.free(2),
            ZModule.free(3),
            ZModule.free(4),
        )
        self.assertEqual(tensor_product.rank, 1 * 2 * 3 * 4)
        self.assertEqual(tensor_product.torsion_numbers, ())

    def test_tensor_product_of_zero_dimensional(self):
        tensor_product = TensorProduct(
            ZModule(0, [6, 48]),
            ZModule(0, [12, 24]),
            ZModule(0, [18]),
        )
        self.assertEqual(tensor_product.rank, 0)
        self.assertEqual(tensor_product.torsion_numbers, (6, 6, 6, 6))

    def test_tensor_product_of_zero_dimensional_trivial(self):
        tensor_product = TensorProduct(
            ZModule(0, [6, 48]),
            ZModule(0, [12, 12, 24]),
            ZModule(0, [18]),
            ZModule(0, [17]),
        )
        self.assertTrue(tensor_product.is_zero())

    def test_tensor_product_with_torsion_mutually_prime(self):
        tensor_product = TensorProduct(
            ZModule(1, [6, 48]),
            ZModule(1, [12, 12, 24]),
            ZModule(1, [18]),
            ZModule(0, [17]),
        )

        self.assertEqual(tensor_product.rank, 0)
        self.assertEqual(tensor_product.torsion_numbers, (17,))

    def test_tensor_product_with_torsion(self):
        tensor_product = TensorProduct(
            ZModule(1, [2, 16]),
            ZModule(1, [4, 8]),
            ZModule(1, [32]),
        )
        self.assertEqual(tensor_product.rank, 1)
        self.assertEqual(
            tensor_product.torsion_numbers,
            (32, 4, 4, 8, 8, 2, 2, 2, 2, 2, 2, 16, 16, 4, 4, 8, 8)
        )

    def test_tensor_product_mixed(self):
        tensor_product = TensorProduct(
            ZModule.free(1),
            ZModule(1, [26]),
            ZModule(3, [13, 52]),
        )

        self.assertEqual(tensor_product.rank, 1 * 1 * 3)
        self.assertEqual(tensor_product.torsion_numbers,
                         (13, 52, 26, 26, 26, 13, 26))

    def test_pure_tensors(self):
        A = ZModule(1, [6])
        B = ZModule(1, [8])
        C = TensorProduct(A, B)

        self.assertEqual(C.rank, 1)
        self.assertEqual(C.torsion_numbers, (8, 6, 2))

        self.assertEqual(
            C.pure_tensor(A.element([0, 0]), B.element([3, 5])).coordinates,
            C.zero_element().coordinates
        )

        self.assertEqual(
            C.pure_tensor(A.element([3, 5]), B.element([0, 0])).coordinates,
            C.zero_element().coordinates
        )

        a = C.pure_tensor(A.element((-10, 9)), B.element((20, 9)))
        b = C.pure_tensor(A.element((1, 1)), B.element((1, 1)))
        c = a + b
        self.assertEqual(str(a), "(-200, 6 + 8ℤ, 0 + 6ℤ, 1 + 2ℤ)")
        self.assertEqual(str(b), "(1, 1 + 8ℤ, 1 + 6ℤ, 1 + 2ℤ)")
        self.assertEqual(str(c), "(-199, 7 + 8ℤ, 1 + 6ℤ, 0 + 2ℤ)")

    def test_pure_tensors_with_mutually_prime(self):
        A = ZModule(1, [7])
        B = ZModule(1, [8])
        C = TensorProduct(A, B)

        self.assertEqual(C.rank, 1)
        self.assertEqual(C.torsion_numbers, (8, 7))

        self.assertEqual(
            str(C.pure_tensor(A.element([1, 1]), B.element([1, 1]))),
            "(1, 1 + 8ℤ, 1 + 7ℤ)"
        )

    def test_pure_tensors_with_zero(self):
        A = ZModule(1, [7])
        B = ZModule(0, [8])
        C = ZModule(1, [9])
        D = TensorProduct(A, B, C)

        self.assertEqual(D.rank, 0)
        self.assertEqual(D.torsion_numbers, (8,))

        self.assertEqual(
            str(D.pure_tensor(
                A.element((1, 2)),
                B.element((3,)),
                C.element((2, 5))
            )),
            "6 + 8ℤ"
        )

    def test_homomorphism_easy(self):
        A = ZModule(1, [7])
        B = ZModule(1, [8])
        A_times_B = TensorProduct(A, B)
        D = ZModule(1, [7 * 8])

        f = Homomorphism([
            [1, 0],
            [0, 1]
        ], A, D)

        g = Homomorphism([
            [-1, 0],
            [0, -1]
        ], B, D)

        f_times_g = A_times_B.homomorphism(f, g)
        self.assertEqual(f_times_g.matrix, (
            (-1, 0, 0),
            (0, 55, 0),
            (0, 0, 55),
            (0, 0, 0)
        ))
        self.assertEqual(f_times_g.domain.rank, A_times_B.rank)
        self.assertEqual(
            f_times_g.domain.torsion_numbers,
            A_times_B.torsion_numbers
        )
        self.assertEqual(f_times_g.codomain.rank, 1)
        self.assertEqual(
            f_times_g.codomain.torsion_numbers,
            (56, 56, 56)
        )

    def test_homomorphism_hard(self):
        A = ZModule(1, [7])
        B = ZModule(1, [8])
        A_times_B = TensorProduct(A, B)
        D = ZModule(1, [7 * 8])

        f = Homomorphism([
            [1, 2],
            [3, 4]
        ], A, D)

        g = Homomorphism([
            [5, 6],
            [7, 8]
        ], B, D)

        f_times_g = A_times_B.homomorphism(f, g)
        self.assertEqual(f_times_g.matrix, (
            (5, 6, 10),
            (7, 8, 14),
            (15, 18, 20),
            (21, 24, 28)
        ))
        self.assertTrue(f_times_g.domain.is_isomorphic_to(A_times_B))
        self.assertEqual(f_times_g.codomain.rank, 1)
        self.assertEqual(
            f_times_g.codomain.torsion_numbers,
            (56, 56, 56)
        )


if __name__ == '__main__':
    unittest.main()

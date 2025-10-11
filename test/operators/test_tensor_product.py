import unittest
from homology.zmodule import ZModule
from homology.cyclic_zmodule import FreeCyclicZModule, TorsionCyclicZModule
from homology.operators.tensor_product import TensorProduct


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
        self.assertEqual(tensor_product.torsion_numbers, [])

    def test_tensor_product_of_zero_dimensional(self):
        tensor_product = TensorProduct(
            ZModule(0, [6, 48]),
            ZModule(0, [12, 24]),
            ZModule(0, [18]),
        )
        self.assertEqual(tensor_product.rank, 0)
        self.assertEqual(tensor_product.torsion_numbers, [6, 6, 6, 6])

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
        self.assertEqual(tensor_product.torsion_numbers, [17])

    def test_tensor_product_with_torsion(self):
        tensor_product = TensorProduct(
            ZModule(1, [2, 16]),
            ZModule(1, [4, 8]),
            ZModule(1, [32]),
        )
        self.assertEqual(tensor_product.rank, 1)
        self.assertEqual(
            tensor_product.torsion_numbers,
            [32, 4, 4, 8, 8, 2, 2, 2, 2, 2, 2, 16, 16, 4, 4, 8, 8]
        )

    def test_tensor_product_mixed(self):
        tensor_product = TensorProduct(
            ZModule.free(1),
            ZModule(1, [26]),
            ZModule(3, [13, 52]),
        )

        self.assertEqual(tensor_product.rank, 1 * 1 * 3)
        self.assertEqual(tensor_product.torsion_numbers,
                         [13, 52, 26, 26, 26, 13, 26])

    def test_pure_tensors(self):
        A = ZModule(1, [6])
        B = ZModule(1, [8])
        C = TensorProduct(A, B)

        self.assertEqual(C.rank, 1)
        self.assertEqual(C.torsion_numbers, [8, 6, 2])

        self.assertEqual(
            C.pure_tensor(A.element([0, 0]), B.element([3, 5])).coordinates,
            C.zero_element().coordinates
        )

        self.assertEqual(
            C.pure_tensor(A.element([3, 5]), B.element([0, 0])).coordinates,
            C.zero_element().coordinates
        )

        a = C.pure_tensor(A.element([-10, 9]), B.element([20, 9]))
        b = C.pure_tensor(A.element([1, 1]), B.element([1, 1]))
        c = a + b
        self.assertEqual(str(a), "(-200, 6 + 8ℤ, 0 + 6ℤ, 1 + 2ℤ)")
        self.assertEqual(str(b), "(1, 1 + 8ℤ, 1 + 6ℤ, 1 + 2ℤ)")
        self.assertEqual(str(c), "(-199, 7 + 8ℤ, 1 + 6ℤ, 0 + 2ℤ)")


if __name__ == '__main__':
    unittest.main()

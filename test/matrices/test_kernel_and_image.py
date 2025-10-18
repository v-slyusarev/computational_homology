import unittest
from module_theory._internal.matrix import Matrix
from module_theory._internal.kernel_and_image import KernelAndImageCalculator


class TestKernelAndImage(unittest.TestCase):

    def test_kernel_and_image(self):
        array = [
            [0, 2, 2],
            [1, 0, -1],
            [3, 4, 1],
            [5, 3, -2]
        ]
        matrix = Matrix(array)
        kernel_and_image_calculator = KernelAndImageCalculator(matrix)
        self.assertEqual(kernel_and_image_calculator.kernel, [
            [1, -1, 1]
        ])
        self.assertEqual(kernel_and_image_calculator.image, [
            [2, 0, 4, 3],
            [0, 1, 3, 5]
        ])

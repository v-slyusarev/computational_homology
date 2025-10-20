import unittest
from module_theory._internal.kernel_and_image import KernelAndImageCalculator


class TestKernelAndImage(unittest.TestCase):

    def test_kernel_and_image(self):
        matrix = [
            [0, 2, 2],
            [1, 0, -1],
            [3, 4, 1],
            [5, 3, -2]
        ]
        kernel_and_image_calculator = KernelAndImageCalculator(matrix)
        self.assertEqual(kernel_and_image_calculator.kernel, [
            [1, -1, 1]
        ])
        self.assertEqual(kernel_and_image_calculator.image, [
            [2, 0, 4, 3],
            [0, 1, 3, 5]
        ])

    def test_kernel_and_image_Z3(self):
        matrix = [
            [3, 2, 3],
            [0, 2, 0],
            [2, 2, 2]
        ]
        kernel_and_image_calculator = KernelAndImageCalculator(matrix)
        self.assertEqual(kernel_and_image_calculator.kernel, [
            [-1, 0, 1]
        ])


if __name__ == '__main__':
    unittest.main()

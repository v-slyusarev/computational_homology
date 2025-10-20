import unittest
from module_theory._internal.matrix import Matrix
from module_theory._internal.row_echelon import RowEchelonCalculator
from module_theory.homomorphism import Homomorphism
from module_theory.zmodule import ZModule


class TestRowEchelon(unittest.TestCase):

    # def test_prepare_row_reduce_step(self):
    #     array = [
    #         [3, 2, 1, 4],
    #         [2, 3, 1, -1],
    #         [4, 4, -2, -2],
    #     ]

    #     matrix = Matrix(array)
    #     row_echelon_calculator = RowEchelonCalculator(matrix)

    #     row_echelon_calculator._prepare_row_reduce_step(0, 0)
    #     self.assertEqual(row_echelon_calculator._array(), [
    #         [2, 3, 1, -1],
    #         [3, 2, 1, 4],
    #         [4, 4, -2, -2],
    #     ])
    #     self.assertEqual(row_echelon_calculator.inverse_change_matrix().array, [
    #         [0, 1, 0],
    #         [1, 0, 0],
    #         [0, 0, 1]
    #     ])
    #     self.assertEqual(row_echelon_calculator.change_matrix().array, [
    #         [0, 1, 0],
    #         [1, 0, 0],
    #         [0, 0, 1]
    #     ])

    # def test_row_reduce(self):
    #     array = [
    #         [3, 2, 1, 4],
    #         [2, 3, 1, -1],
    #         [4, 4, -2, -2],
    #     ]

    #     matrix = Matrix(array)
    #     row_echelon_calculator = RowEchelonCalculator(matrix)

    #     row_echelon_calculator._row_reduce(0, 0)
    #     self.assertEqual(row_echelon_calculator._array(), [
    #         [1, -1, 0, 5],
    #         [0, 5, 1, -11],
    #         [0, -2, -4, 0],
    #     ])
    #     self.assertEqual(row_echelon_calculator.inverse_change_matrix().array, [
    #         [1, -1, 0],
    #         [-2, 3, 0],
    #         [0, -2, 1]
    #     ])
    #     self.assertEqual(row_echelon_calculator.change_matrix().array, [
    #         [3, 1, 0],
    #         [2, 1, 0],
    #         [4, 2, 1]
    #     ])

    def test_row_echelon(self):
        array = (
            (3, 2, 1, 4),
            (2, 3, 1, -1),
            (4, 4, -2, -2),
        )

        matrix = Matrix(array)
        row_echelon_calculator = RowEchelonCalculator(matrix)

        self.assertEqual(row_echelon_calculator.row_echelon().array, [
            [1, -1, 0, 5],
            [0, -1, -11, -11],
            [0, 0, 18, 22],
        ])
        self.assertEqual(
            row_echelon_calculator.inverse_change_matrix().array,
            [
                [1, -1, 0],
                [-2, -3, 3],
                [4, 4, -5]
            ])
        self.assertEqual(row_echelon_calculator.change_matrix().array, [
            [3, -5, -3],
            [2, -5, -3],
            [4, -8, -5]
        ])

        self.assertEqual(row_echelon_calculator.row_rank(), 3)
        homomorphism = Homomorphism(array)
        change_homomorphism = Homomorphism(
            row_echelon_calculator.change_matrix().array)
        inverse_change_homomorphism = Homomorphism(
            row_echelon_calculator.inverse_change_matrix().array)
        result_homomorphism = Homomorphism(row_echelon_calculator._array())

        self.assertEqual(
            inverse_change_homomorphism.compose(change_homomorphism).matrix,
            Homomorphism.identity(ZModule.free(3)).matrix
        )

        self.assertEqual(
            change_homomorphism.compose(inverse_change_homomorphism).matrix,
            Homomorphism.identity(ZModule.free(3)).matrix
        )

        self.assertEqual(
            inverse_change_homomorphism.compose(homomorphism).matrix,
            Homomorphism(row_echelon_calculator.row_echelon().array).matrix
        )

        self.assertEqual(
            change_homomorphism.compose(result_homomorphism).matrix,
            array
        )

    def test_row_echelon_zero(self):
        array = (
            (0, 0, 0),
            (0, 0, 0),
        )

        matrix = Matrix(array)
        row_echelon_calculator = RowEchelonCalculator(matrix)
        row_echelon_calculator.row_echelon()

        self.assertEqual(row_echelon_calculator.row_echelon().array, [
            [0, 0, 0],
            [0, 0, 0],
        ])
        self.assertEqual(
            row_echelon_calculator.inverse_change_matrix().array,
            [
                [1, 0],
                [0, 1],
            ])
        self.assertEqual(row_echelon_calculator.change_matrix().array, [
            [1, 0],
            [0, 1],
        ])
        self.assertEqual(row_echelon_calculator.row_rank(), 0)

    def test_row_echelon_noop(self):
        array = (
            (1, 0, 0),
            (0, 0, 0),
        )

        matrix = Matrix(array)
        row_echelon_calculator = RowEchelonCalculator(matrix)

        row_echelon_calculator.row_echelon()

        self.assertEqual(row_echelon_calculator.row_echelon().array, [
            [1, 0, 0],
            [0, 0, 0],
        ]
        )
        self.assertEqual(
            row_echelon_calculator.inverse_change_matrix().array,
            [
                [1, 0],
                [0, 1],
            ]
        )
        self.assertEqual(row_echelon_calculator.change_matrix().array, [
            [1, 0],
            [0, 1],
        ])
        self.assertEqual(row_echelon_calculator.row_rank(), 1)

    def test_row_echelon_swap(self):
        array = (
            (0, 0, 0),
            (0, 0, 1),
        )

        matrix = Matrix(array)
        row_echelon_calculator = RowEchelonCalculator(matrix)

        row_echelon_calculator.row_echelon()

        self.assertEqual(row_echelon_calculator.row_echelon().array, [
            [0, 0, 1],
            [0, 0, 0],
        ])
        self.assertEqual(
            row_echelon_calculator.inverse_change_matrix().array,
            [
                [0, 1],
                [1, 0],
            ]
        )
        self.assertEqual(row_echelon_calculator.change_matrix().array, [
            [0, 1],
            [1, 0],
        ])
        self.assertEqual(row_echelon_calculator.row_rank(), 1)

    def test_row_echelon_degenerate(self):
        array = [
            [3, 0, 2],
            [2, 2, 2],
            [3, 0, 2]
        ]

        matrix = Matrix(array)
        row_echelon_calculator = RowEchelonCalculator(matrix)

        row_echelon_calculator.row_echelon()

        self.assertEqual(row_echelon_calculator.row_echelon().array, [
            [1, -2, 0],
            [0, 6, 2],
            [0, 0, 0],
        ])
        self.assertEqual(
            row_echelon_calculator.inverse_change_matrix().array,
            [
                [1, -1, 0],
                [-2, 3, 0],
                [-1, 0, 1]
            ]
        )
        self.assertEqual(row_echelon_calculator.change_matrix().array, [
            [3, 1, 0],
            [2, 1, 0],
            [3, 1, 1],
        ])
        self.assertEqual(row_echelon_calculator.row_rank(), 2)

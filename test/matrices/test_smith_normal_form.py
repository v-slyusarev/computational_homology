import unittest
from module_theory._internal.matrix import Matrix
from module_theory._internal.smith_normal_form import SmithNormalFormCalculator
# from module_theory.homomorphism import Homomorphism


class TestSmithNormalForm(unittest.TestCase):
    def test_move(self):
        array = [
            [9, 8, 7],
            [-4, 0, 3],
            [0, -10, -2]
        ]
        matrix = Matrix(array)
        calculator = SmithNormalFormCalculator(
            matrix, calculate_instantly=False
        )
        calculator._move_minimal_nonzero_entry(1)
        self.assertEqual(
            calculator._array(),
            [
                [9, 7, 8],
                [0, -2, -10],
                [-4, 3, 0],
            ]
        )

    def test_find_nondivisible_entry_negative(self):
        array = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ]
        matrix = Matrix(array)
        calculator = SmithNormalFormCalculator(
            matrix, calculate_instantly=False
        )
        result = calculator._find_nondivisible_entry(0)
        self.assertIsNone(result)

    def test_find_nondivisible_entry_positive(self):
        array = [
            [1, 2, 3],
            [4, 5, -10],
            [7, -8, 15]
        ]
        matrix = Matrix(array)
        calculator = SmithNormalFormCalculator(
            matrix, calculate_instantly=False
        )
        result = calculator._find_nondivisible_entry(1)
        self.assertEqual(result, (2, 1, -2))

    def test_smith_normal_form_step(self):
        array = [
            [9, 8, 7],
            [6, 5, 4],
            [7, 8, 9]
        ]
        matrix = Matrix(array)
        calculator = SmithNormalFormCalculator(
            matrix, calculate_instantly=False
        )
        calculator._smith_normal_form_step(0)
        self.assertEqual(calculator._array(), [
            [1, 0, 0],
            [0, 9, 18],
            [0, 13, 26]
        ])
        self.assertEqual(calculator.row_change_matrix().array, [
            [7, 1, 1],
            [4, 0, 1],
            [9, 0, 2]
        ])
        self.assertEqual(calculator.inverse_row_change_matrix().array, [
            [0, -2, 1],
            [1, 5, -3],
            [0, 9, -4]
        ])
        self.assertEqual(calculator.column_change_matrix().array, [
            [0, 0, 1],
            [0, 1, 0],
            [1, 2, 5]
        ])
        self.assertEqual(calculator.inverse_column_change_matrix().array, [
            [-5, -2, 1],
            [0, 1, 0],
            [1, 0, 0]
        ])

        # homomorphism = Homomorphism(array)
        # row_change_homomorphism = Homomorphism(
        #     calculator.row_change_matrix().array
        # )
        # inverse_row_change_homomorphism = Homomorphism(
        #     calculator.inverse_row_change_matrix().array
        # )
        # column_change_homomorphism = Homomorphism(
        #     calculator.column_change_matrix().array
        # )
        # inverse_column_change_homomorphism = Homomorphism(
        #     calculator.inverse_column_change_matrix().array
        # )
        # result_homomorphism = Homomorphism(calculator._array())

        # self.assertEqual(
        #     inverse_row_change_homomorphism.compose(
        #         row_change_homomorphism
        #     ).matrix,
        #     Homomorphism.identity(row_change_homomorphism.domain).matrix
        # )

        # self.assertEqual(
        #     row_change_homomorphism.compose(
        #         inverse_row_change_homomorphism
        #         ).matrix,
        #     Homomorphism.identity(row_change_homomorphism.codomain).matrix
        # )

        # self.assertEqual(
        #     inverse_column_change_homomorphism.compose(
        #         column_change_homomorphism
        #     ).matrix,
        #     Homomorphism.identity(column_change_homomorphism.domain).matrix
        # )

        # self.assertEqual(
        #     column_change_homomorphism.compose(
        #         inverse_column_change_homomorphism
        #         ).matrix,
        #     Homomorphism.identity(column_change_homomorphism.codomain).matrix
        # )

        # self.assertEqual(
        #     inverse_row_change_homomorphism
        #     .compose(homomorphism)
        #     .compose(column_change_homomorphism).matrix,
        #     result_homomorphism.matrix
        # )

    def test_smith_normal_form(self):
        array = [
            [3, 2, 3],
            [0, 2, 0],
            [2, 2, 2]
        ]
        matrix = Matrix(array)
        calculator = SmithNormalFormCalculator(matrix)
        # calculator._smith_normal_form_step(0)
        self.assertEqual(calculator._array(), [
            [1, 0, 0],
            [0, 2, 0],
            [0, 0, 0]
        ])
        self.assertEqual(calculator.inverse_row_change_matrix().array, [
            [1, 0, 0],
            [0, 0, 1],
            [2, 1, -3]
        ])
        self.assertEqual(calculator.row_change_matrix().array, [
            [1, 0, 0],
            [-2, 3, 1],
            [0, 1, 0]
        ])
        self.assertEqual(calculator.column_change_matrix().array, [
            [1, -2, -1],
            [-1, 3, 0],
            [0, 0, 1]
        ])
        self.assertEqual(calculator.inverse_column_change_matrix().array, [
            [3, 2, 3],
            [1, 1, 1],
            [0, 0, 1]
        ])


if __name__ == '__main__':
    unittest.main()

import unittest
from module_theory._internal.matrix import Matrix
from module_theory._internal.matrix_manipulator import MatrixManipulator


class TestMatrixManipulator(unittest.TestCase):
    def test_matrix_manipulator_init(self):
        array = [
            [2, 3, 1, -1],
            [3, 2, 1, 4],
            [4, 4, -2, -2],
        ]
        matrix = Matrix(array)
        matrix_manipulator = MatrixManipulator(matrix)
        self.assertEqual(matrix_manipulator.matrix.array, array)
        self.assertEqual(matrix_manipulator.row_change_matrix.array, [
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 1]
        ])
        self.assertEqual(matrix_manipulator.inverse_row_change_matrix.array, [
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 1]
        ])

    def test_exchange_rows(self):
        array = [
            [2, 3, 1, -1],
            [3, 2, 1, 4],
            [4, 4, -2, -2],
        ]
        matrix_manipulator = MatrixManipulator(Matrix(array))
        matrix_manipulator.exchange_rows(0, 1)
        self.assertEqual(matrix_manipulator.matrix.array, [
            [3, 2, 1, 4],
            [2, 3, 1, -1],
            [4, 4, -2, -2],
        ])
        self.assertEqual(matrix_manipulator.inverse_row_change_matrix.array, [
            [0, 1, 0],
            [1, 0, 0],
            [0, 0, 1]
        ])
        self.assertEqual(matrix_manipulator.row_change_matrix.array, [
            [0, 1, 0],
            [1, 0, 0],
            [0, 0, 1]
        ])

    def test_add_multiple_of_row(self):
        array = [
            [2, 3, 1, -1],
            [3, 2, 1, 4],
            [4, 4, -2, -2],
        ]
        matrix_manipulator = MatrixManipulator(Matrix(array))
        matrix_manipulator.add_multiple_of_row(1, 0, -1)
        self.assertEqual(matrix_manipulator.matrix.array, [
            [2, 3, 1, -1],
            [1, -1, 0, 5],
            [4, 4, -2, -2],
        ])
        self.assertEqual(matrix_manipulator.inverse_row_change_matrix.array, [
            [1, 0, 0],
            [-1, 1, 0],
            [0, 0, 1]
        ])
        self.assertEqual(matrix_manipulator.row_change_matrix.array, [
            [1, 0, 0],
            [1, 1, 0],
            [0, 0, 1]
        ])

    def test_reduce_rows_by_pivot(self):
        array = [
            [2, 3, 1, -1],
            [3, 2, 1, 4],
            [4, 4, -2, -2],
        ]

        matrix = Matrix(array)
        matrix_manipulator = MatrixManipulator(matrix)

        matrix_manipulator.reduce_rows_by_pivot(0, 0)
        self.assertEqual(matrix_manipulator._array(), [
            [2, 3, 1, -1],
            [1, -1, 0, 5],
            [0, -2, -4, 0]
        ])
        self.assertEqual(matrix_manipulator.inverse_row_change_matrix.array, [
            [1, 0, 0],
            [-1, 1, 0],
            [-2, 0, 1]
        ])
        self.assertEqual(matrix_manipulator.row_change_matrix.array, [
            [1, 0, 0],
            [1, 1, 0],
            [2, 0, 1]
        ])

    def test_reduce_columns_by_pivot(self):
        array = [
            [2, 3, 4],
            [3, 2, 4],
            [1, 1, -2],
            [-1, 4, -2]
        ]

        matrix = Matrix(array)
        matrix_manipulator = MatrixManipulator(matrix)

        matrix_manipulator.reduce_columns_by_pivot(0, 0)
        self.assertEqual(matrix_manipulator._array(), [
            [2, 1, 0],
            [3, -1, -2],
            [1, 0, -4],
            [-1, 5, 0]
        ])
        self.assertEqual(
            matrix_manipulator.inverse_column_change_matrix.array,
            [
                [1, 1, 2],
                [0, 1, 0],
                [0, 0, 1]
            ]
        )
        self.assertEqual(matrix_manipulator.column_change_matrix.array, [
            [1, -1, -2],
            [0, 1, 0],
            [0, 0, 1]
        ])


if __name__ == '__main__':
    unittest.main()

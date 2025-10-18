import unittest
from module_theory._internal.matrix import Matrix


class TestMatrix(unittest.TestCase):
    def test_exchange_rows(self):
        matrix = Matrix([
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ])

        matrix.exchange_rows(0, 2)

        self.assertEqual(matrix.array, [
            [7, 8, 9],
            [4, 5, 6],
            [1, 2, 3]
        ])

        matrix.exchange_rows(1, 1)

        self.assertEqual(matrix.array, [
            [7, 8, 9],
            [4, 5, 6],
            [1, 2, 3]
        ])

        matrix.exchange_rows(0, 2)

        self.assertEqual(matrix.array, [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ])

    def test_exchange_columns(self):
        matrix = Matrix([
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ])

        matrix.exchange_columns(0, 2)

        self.assertEqual(matrix.array, [
            [3, 2, 1],
            [6, 5, 4],
            [9, 8, 7]
        ])

        matrix.exchange_columns(1, 1)

        self.assertEqual(matrix.array, [
            [3, 2, 1],
            [6, 5, 4],
            [9, 8, 7]
        ])

        matrix.exchange_columns(0, 2)

        self.assertEqual(matrix.array, [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ])

    def test_multiply_row_by_negative_one(self):
        matrix = Matrix([
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ])

        matrix.multiply_row_by_negative_one(1)

        self.assertEqual(matrix.array, [
            [1, 2, 3],
            [-4, -5, -6],
            [7, 8, 9]
        ])

        matrix.multiply_row_by_negative_one(0)

        self.assertEqual(matrix.array, [
            [-1, -2, -3],
            [-4, -5, -6],
            [7, 8, 9]
        ])

        matrix.multiply_row_by_negative_one(1)

        self.assertEqual(matrix.array, [
            [-1, -2, -3],
            [4, 5, 6],
            [7, 8, 9]
        ])

        matrix.multiply_row_by_negative_one(0)

        self.assertEqual(matrix.array, [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ])

    def test_multiply_column_by_negative_one(self):
        matrix = Matrix([
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ])

        matrix.multiply_column_by_negative_one(1)

        self.assertEqual(matrix.array, [
            [1, -2, 3],
            [4, -5, 6],
            [7, -8, 9]
        ])

        matrix.multiply_column_by_negative_one(0)

        self.assertEqual(matrix.array, [
            [-1, -2, 3],
            [-4, -5, 6],
            [-7, -8, 9]
        ])

        matrix.multiply_column_by_negative_one(1)

        self.assertEqual(matrix.array, [
            [-1, 2, 3],
            [-4, 5, 6],
            [-7, 8, 9]
        ])

        matrix.multiply_column_by_negative_one(0)

        self.assertEqual(matrix.array, [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ])

    def test_add_row(self):
        matrix = Matrix([
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ])

        matrix.add_multiple_of_row(0, 1, 100)

        self.assertEqual(matrix.array, [
            [401, 502, 603],
            [4, 5, 6],
            [7, 8, 9]
        ])

    def test_add_multiple_of_column(self):
        matrix = Matrix([
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ])

        matrix.add_multiple_of_column(2, 1, 100)

        self.assertEqual(matrix.array, [
            [1, 2, 203],
            [4, 5, 506],
            [7, 8, 809]
        ])

    def test_transpose(self):
        matrix = Matrix([
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ])

        matrix.transpose()

        self.assertEqual(matrix.array, [
            [1, 4, 7],
            [2, 5, 8],
            [3, 6, 9]
        ])


if __name__ == '__main__':
    unittest.main()

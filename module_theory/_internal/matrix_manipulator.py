from module_theory._internal.matrix import Matrix


class MatrixManipulator:
    def __init__(self, matrix: Matrix):
        self._matrix: Matrix = matrix

        self._row_change_matrix: Matrix = (
            self._trivial_change_matrix(self.row_count())
        )
        self._inverse_row_change_matrix: Matrix = (
            self._trivial_change_matrix(self.row_count())
        )
        self._column_change_matrix: Matrix = (
            self._trivial_change_matrix(self.column_count())
        )
        self._inverse_column_change_matrix: Matrix = (
            self._trivial_change_matrix(self.column_count())
        )

    @property
    def matrix(self) -> Matrix:
        return self._matrix

    @property
    def row_change_matrix(self) -> Matrix:
        return self._row_change_matrix

    @property
    def inverse_row_change_matrix(self) -> Matrix:
        return self._inverse_row_change_matrix

    @property
    def column_change_matrix(self) -> Matrix:
        return self._column_change_matrix

    @property
    def inverse_column_change_matrix(self) -> Matrix:
        return self._inverse_column_change_matrix

    def _array(self) -> list[list[int]]:
        return self._matrix.array

    def row_count(self) -> int:
        return self._matrix.row_count()

    def column_count(self) -> int:
        return self._matrix.column_count()

    def exchange_rows(self, first_index: int, second_index: int):
        self.matrix.exchange_rows(first_index, second_index)
        self.inverse_row_change_matrix.exchange_rows(first_index, second_index)
        self.row_change_matrix.exchange_columns(first_index, second_index)

    def exchange_columns(self, first_index: int, second_index: int):
        self.matrix.exchange_columns(first_index, second_index)
        self.inverse_column_change_matrix.exchange_columns(first_index, second_index)
        self.column_change_matrix.exchange_columns(first_index, second_index)

    def multiply_row_by_negative_one(self, row_index: int):
        self.matrix.multiply_row_by_negative_one(row_index)
        self.inverse_row_change_matrix.multiply_row_by_negative_one(row_index)
        self.row_change_matrix.multiply_column_by_negative_one(row_index)

    def add_multiple_of_row(
        self, add_to_index: int, add_index: int, multiplier: int = 1
    ):
        if add_to_index == add_index and multiplier == -1:
            self._row_rank = None

        self.matrix.add_multiple_of_row(add_to_index, add_index, multiplier)
        self.inverse_row_change_matrix.add_multiple_of_row(add_to_index,
                                                       add_index, multiplier)
        self.row_change_matrix.add_multiple_of_column(add_index,
                                                  add_to_index, -multiplier)

    @staticmethod
    def _trivial_change_matrix(row_count: int) -> Matrix:
        return Matrix([
            [1 if row == column else 0 for column in range(row_count)]
            for row in range(row_count)
        ])

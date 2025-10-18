from module_theory._internal.matrix import Matrix
from module_theory._internal.matrix_manipulator import MatrixManipulator


class RowEchelonCalculator:
    def __init__(self, matrix: Matrix):
        self._matrix_manipulator: MatrixManipulator = MatrixManipulator(matrix)
        self._complete = False
        self._calculate()
        self._complete = True

    def row_echelon(self) -> Matrix:
        if not self._complete:
            raise RuntimeError("Not calculated yet")
        return self._matrix_manipulator.matrix

    def change_matrix(self) -> Matrix:
        return self._matrix_manipulator.row_change_matrix

    def inverse_change_matrix(self) -> Matrix:
        return self._matrix_manipulator.inverse_row_change_matrix

    def row_rank(self) -> int:
        return self._row_rank

    def _array(self) -> list[list[int]]:
        return self._matrix_manipulator.matrix.array

    def _row_count(self) -> int:
        return self._matrix_manipulator.matrix.row_count()

    def _column_count(self) -> int:
        return self._matrix_manipulator.matrix.column_count()

    def _row_reduce_step(
        self, pivot_row_index: int, pivot_column_index: int
    ):
        pivot_value: int = (
            self._array()[pivot_row_index][pivot_column_index]
        )

        for row_index in range(pivot_row_index + 1, self._row_count()):
            multiplier: int = (
                self._array()[row_index][pivot_column_index] // pivot_value
            )
            self._matrix_manipulator.add_multiple_of_row(
                row_index, pivot_row_index, -multiplier
            )

    def _prepare_row_reduce_step(
        self, pivot_row_index: int, pivot_column_index: int
    ):
        pivot_column_nonzero_entries = [
            (index, abs(row[pivot_column_index]))
            for (index, row) in enumerate(self._array())
            if index >= pivot_row_index and row[pivot_column_index] != 0
        ]
        min_nonzero_entry = min([
            value for (_, value) in pivot_column_nonzero_entries
        ])
        for (index, entry) in pivot_column_nonzero_entries:
            if entry == min_nonzero_entry:
                print(f"Min nonzero = {min_nonzero_entry} at {index}")
                self._matrix_manipulator.exchange_rows(pivot_row_index, index)
                return

        raise Exception("Found no nonzero entry in pivot column")

    def _row_reduce(self, pivot_row_index: int, pivot_column_index: int):
        while any(row[pivot_column_index] != 0
                  for row in self._array()[pivot_row_index + 1:]):
            print(f'row_reduce called for {pivot_row_index}, {pivot_column_index}\n',
                  '\n'.join([str(row) for row in self._array()]))
            self._prepare_row_reduce_step(pivot_row_index, pivot_column_index)
            self._row_reduce_step(pivot_row_index, pivot_column_index)

    def _calculate(self) -> None:
        pivot_row_index = 0
        pivot_column_index = 0

        # if self.matrix.is_zero():
        #     self._row_rank = 0
        #     return

        # self.row_rank = 1
        while pivot_row_index < self._row_count():
            # print(f'\n==========STEP {pivot_row_index}==========')
            # homomorphism = Homomorphism(self.array())
            # print("B = ", homomorphism)
            # change_homomorphism = Homomorphism(self.change_matrix.array)
            # print("Q = ", change_homomorphism)
            # inverse_change_homomorphism = Homomorphism(self.inverse_change_matrix.array)
            # print("Qinv = ", inverse_change_homomorphism)

            # print("QinvQ = ", inverse_change_homomorphism.compose(change_homomorphism))
            # print("QQinv = ", change_homomorphism.compose(inverse_change_homomorphism))
            # print("QB = ", change_homomorphism.compose(homomorphism))

            while pivot_column_index < self._column_count() and all(
                row[pivot_column_index] == 0
                for row in self._array()[pivot_row_index:]
            ):
                pivot_column_index += 1

            if pivot_column_index >= self._column_count():
                break

            self._row_reduce(pivot_row_index, pivot_column_index)
            pivot_row_index += 1

        self._row_rank = pivot_row_index

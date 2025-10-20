from __future__ import annotations
from collections.abc import Sequence
from module_theory._internal.matrix import Matrix
from module_theory._internal.matrix_manipulator import MatrixManipulator
from dataclasses import dataclass


class SmithNormalFormCalculator:
    def __init__(self, array: Sequence[Sequence[int]],
                 /, calculate_instantly: bool = True):
        matrix = Matrix(array)
        self._matrix_manipulator: MatrixManipulator = MatrixManipulator(matrix)
        self._complete = False
        if calculate_instantly:
            self._calculate()
        self._complete = True

    def smith_normal_form(self) -> SmithNormalForm:
        if not self._complete:
            raise RuntimeError("Not calculated yet")
        matrix = self._matrix_manipulator.matrix.immutable()
        return SmithNormalForm(
            matrix=matrix,
            diagonal=tuple(
                row[row_index] for row_index, row
                in enumerate(matrix[:self.rank()])
            ),
            row_change_matrix=self._row_change_matrix().immutable(),
            inverse_row_change_matrix=(self._inverse_row_change_matrix()
                                           .immutable()),
            column_change_matrix=self._column_change_matrix().immutable(),
            inverse_column_change_matrix=(self._inverse_column_change_matrix()
                                              .immutable()),
            rank=self.rank(),
            unit_entry_count=self.unit_entry_count()
        )

    def _row_change_matrix(self) -> Matrix:
        return self._matrix_manipulator.row_change_matrix

    def _inverse_row_change_matrix(self) -> Matrix:
        return self._matrix_manipulator.inverse_row_change_matrix

    def _column_change_matrix(self) -> Matrix:
        return self._matrix_manipulator.column_change_matrix

    def _inverse_column_change_matrix(self) -> Matrix:
        return self._matrix_manipulator.inverse_column_change_matrix

    def rank(self) -> int:
        if not self._complete:
            raise RuntimeError("Not calculated yet")
        return self._rank

    def unit_entry_count(self) -> int:
        if not self._complete:
            raise RuntimeError("Not calculated yet")
        return self._unit_entry_count

    def _array(self) -> list[list[int]]:
        return self._matrix_manipulator.matrix.array

    def _row_count(self) -> int:
        return self._matrix_manipulator.matrix.row_count()

    def _column_count(self) -> int:
        return self._matrix_manipulator.matrix.column_count()

    def _move_minimal_nonzero_entry(self, pivot_index: int):
        min_nonzero_value = None
        min_nonzero_value_row = pivot_index
        min_nonzero_value_column = pivot_index

        for row_index, row in enumerate(self._array()):
            if row_index < pivot_index:
                continue
            for column_index, value in enumerate(row):
                if column_index < pivot_index:
                    continue
                if value == 0:
                    continue
                if not min_nonzero_value or abs(value) < min_nonzero_value:
                    min_nonzero_value = value
                    min_nonzero_value_row = row_index
                    min_nonzero_value_column = column_index

        if not min_nonzero_value:
            raise Exception("Found no nonzero entry")

        self._matrix_manipulator.exchange_rows(
            pivot_index, min_nonzero_value_row
        )
        self._matrix_manipulator.exchange_columns(
            pivot_index, min_nonzero_value_column
        )

    def _find_nondivisible_entry(self, pivot_index: int) -> tuple[int, int,
                                                                  int] | None:
        pivot = self._array()[pivot_index][pivot_index]

        for row_index, row in enumerate(self._array()):
            if row_index < pivot_index:
                continue
            for column_index, value in enumerate(row):
                if column_index < pivot_index:
                    continue
                if value % pivot:
                    return row_index, column_index, value // pivot

        return None

    def _smith_normal_form_step(self, pivot_index: int):
        while True:
            self._move_minimal_nonzero_entry(pivot_index)
            self._matrix_manipulator.reduce_rows_by_pivot(
                pivot_index, pivot_index
            )
            if any(row[pivot_index] for row in self._array()[pivot_index+1:]):
                continue
            self._matrix_manipulator.reduce_columns_by_pivot(
                pivot_index, pivot_index
            )
            if any(self._array()[pivot_index][pivot_index+1:]):
                continue

            nondivisible_entry = self._find_nondivisible_entry(pivot_index)
            if nondivisible_entry is None:
                return

            (nondivisible_row, nondivisible_column,
             quotient) = nondivisible_entry

            self._matrix_manipulator.add_multiple_of_row(
                nondivisible_row, pivot_index, 1
            )
            self._matrix_manipulator.add_multiple_of_column(
                pivot_index, nondivisible_column, quotient
            )

    def _calculate(self):
        pivot_index = 0
        self._unit_entry_count = 0

        while any(
            value
            for row in self._array()[pivot_index:]
            for value in row[pivot_index:]
        ):
            self._smith_normal_form_step(pivot_index)

            if self._array()[pivot_index][pivot_index] < 0:
                self._matrix_manipulator.multiply_row_by_negative_one(
                    pivot_index
                )

            if self._array()[pivot_index][pivot_index] == 1:
                self._unit_entry_count += 1

            pivot_index += 1

        self._rank = pivot_index


@dataclass(frozen=True)
class SmithNormalForm:
    matrix: tuple[tuple[int, ...], ...]
    diagonal: tuple[int, ...]
    row_change_matrix: tuple[tuple[int, ...], ...]
    inverse_row_change_matrix: tuple[tuple[int, ...], ...]
    column_change_matrix: tuple[tuple[int, ...], ...]
    inverse_column_change_matrix: tuple[tuple[int, ...], ...]
    rank: int
    unit_entry_count: int

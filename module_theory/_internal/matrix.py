from collections.abc import Sequence


class Matrix:
    def __init__(self, array: Sequence[Sequence[int]]):
        self.array: list[list[int]] = list(
            list(row) for row in array
        )

    def row_count(self) -> int:
        return len(self.array)

    def column_count(self) -> int:
        return len(self.array[0])

    def is_zero(self):
        return all(not value for row in self.array for value in row)

    def exchange_rows(self, first_index: int, second_index: int):
        self.array[first_index], self.array[second_index] = (
            self.array[second_index], self.array[first_index]
        )

    def exchange_columns(self, first_index: int, second_index: int):
        for row in self.array:
            row[first_index], row[second_index] = (
                row[second_index], row[first_index]
            )

    def multiply_row_by_negative_one(self, row_index: int):
        for column_index in range(self.column_count()):
            self.array[row_index][column_index] *= -1

    def multiply_column_by_negative_one(self, column_index: int):
        for row_index in range(self.row_count()):
            self.array[row_index][column_index] *= -1

    def add_multiple_of_row(
        self, add_to_index: int, add_index: int, multiplier: int = 1
    ):
        for column_index, add_value in enumerate(self.array[add_index]):
            self.array[add_to_index][column_index] += multiplier * add_value

    def add_multiple_of_column(
        self, add_to_index: int, add_index: int, multiplier: int = 1
    ):
        for row_index in range(self.row_count()):
            self.array[row_index][add_to_index] += (
                multiplier * self.array[row_index][add_index]
            )

    def transpose(self):
        self.array = [
            list(column)
            for column in zip(*self.array)
        ]

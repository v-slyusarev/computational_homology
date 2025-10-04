from collections.abc import Sequence

class Homomorphism:
    def __init__(self,
                 matrix: Sequence[Sequence[int]]):

        if not matrix or not matrix[0]:
            raise ValueError(
                "matrix must be a 2d list with at least one entry"
            )

        dimensions_from = len(matrix[0])

        if any(len(row) != dimensions_from for row in matrix):
            raise ValueError(
                "All rows of matrix must have equal length"
            )

        self.matrix = matrix

    @classmethod
    def dimensions_to(self):
        return len(self.matrix)

    @classmethod
    def dimensions_from(self):
        return len(self.matrix[0])


def zero_homomorphism(dimensions_from: int,
                      dimensions_to: int) -> Homomorphism:
    return Homomorphism([[0 for _ in range(dimensions_from)]
                         for _ in range(dimensions_to)])

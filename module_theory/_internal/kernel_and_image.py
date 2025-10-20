from __future__ import annotations
from collections.abc import Sequence
from module_theory._internal.matrix import Matrix
from module_theory._internal.row_echelon import RowEchelonCalculator


class KernelAndImageCalculator:
    def __init__(self, array: Sequence[Sequence[int]]):
        matrix = Matrix(array)
        matrix.transpose()
        calculator = RowEchelonCalculator(matrix)
        self.kernel = (calculator.inverse_change_matrix()
                                 .array[calculator.row_rank():])
        self.image = (calculator.row_echelon()
                                .array[:calculator.row_rank()])

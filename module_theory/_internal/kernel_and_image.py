from __future__ import annotations
from module_theory._internal.matrix import Matrix
from module_theory._internal.row_echelon import RowEchelonCalculator


class KernelAndImageCalculator:
    def __init__(self, matrix: Matrix):
        matrix.transpose()
        row_echelon_calculator = RowEchelonCalculator(matrix)
        self.kernel = row_echelon_calculator.change_matrix().array[row_echelon_calculator.row_rank():]
        # image_matrix = Matrix(row_echelon_calculator.row_echelon().array)
        # print("image_matrix", image_matrix.array)
        # image_matrix.transpose()
        self.image = row_echelon_calculator.row_echelon().array[:row_echelon_calculator.row_rank()]

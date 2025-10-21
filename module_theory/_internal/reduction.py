from collections.abc import Sequence
from module_theory.zmodule import ZModule
from module_theory._internal.matrix import Matrix
from module_theory._internal.row_echelon import RowEchelonCalculator


def reduction(elements: Sequence[ZModule.Element]) -> list[ZModule.Element]:
    if not elements:
        return []

    matrix = Matrix([
        element.coordinates for element in elements
    ])

    reduced_matrix = RowEchelonCalculator(matrix).row_echelon()

    module = elements[0].module

    reduced_elements = [
        module.element(row) for row in reduced_matrix.array
    ]

    return [reduced_elements[0]] + [
        element for element in reduced_elements[1:] if not element.is_zero()
    ]


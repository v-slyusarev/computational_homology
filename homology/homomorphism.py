from __future__ import annotations
from collections.abc import Sequence
from homology.zmodule import FinitelyGeneratedZModule


class Homomorphism:
    def __init__(self,
                 matrix: Sequence[Sequence[int]],
                 domain: FinitelyGeneratedZModule = None,
                 codomain: FinitelyGeneratedZModule = None):

        if not matrix or not matrix[0]:
            raise ValueError(
                "matrix must be a 2d list with at least one entry"
            )

        self.matrix = matrix

        domain_dimensions = len(matrix[0])

        if any(len(row) != domain_dimensions for row in matrix):
            raise ValueError(
                "All rows of matrix must have equal length"
            )

        if domain is None:
            self.domain = FinitelyGeneratedZModule.free(domain_dimensions)
        elif domain_dimensions != domain.dimensions():
            raise ValueError(
                "domain dimension mismatch"
            )
        else:
            self.domain = domain

        codomain_dimensions = len(matrix)

        if codomain is None:
            self.codomain = FinitelyGeneratedZModule.free(codomain_dimensions)
        elif codomain_dimensions != codomain.dimensions():
            raise ValueError(
                f"codomain dimension mismatch: "
                f"expected {codomain.dimensions()}, "
                f"found {codomain_dimensions}"
            )
        else:
            self.codomain = codomain

    @staticmethod
    def zero(domain: FinitelyGeneratedZModule,
             codomain: FinitelyGeneratedZModule) -> Homomorphism:
        return Homomorphism([[0 for _ in range(domain.dimensions())]
                             for _ in range(codomain.dimensions())])

    @staticmethod
    def identity(module: FinitelyGeneratedZModule) -> Homomorphism:
        return Homomorphism(
            matrix=[[1 if row == column else 0
                    for column in range(module.dimensions())]
                    for row in range(module.dimensions())],
            domain=module,
            codomain=module
        )

    def apply(
        self,
        element: FinitelyGeneratedZModule.Element
    ) -> FinitelyGeneratedZModule.Element:
        if len(element.coordinates) != self.domain.dimensions():
            raise ValueError("dimension mismatch")
        return self.codomain.element([
            sum(element_coordinate * basis_images
                for (element_coordinate, basis_images) in zip(
                    element.coordinates, row
                ))
            for row in self.matrix])

    def compose(self, other: Homomorphism) -> Homomorphism:
        if (
            self.domain.rank != other.codomain.rank or
            self.domain.torsion_numbers != other.codomain.torsion_numbers
        ):
            raise ValueError("domain and codomain mismatch")

        return Homomorphism(
            matrix=[[
                sum(self.matrix[row_index][k] * other.matrix[k][column_index]
                    for k in range(self.domain.dimensions()))
                for column_index in range(other.domain.dimensions())
            ] for row_index in range(self.codomain.dimensions())],
            domain=self.domain,
            codomain=other.codomain
        )

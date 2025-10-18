from __future__ import annotations
from collections.abc import Sequence

from module_theory.zmodule import ZModule


class Homomorphism:
    def __init__(self,
                 matrix: Sequence[Sequence[int]],
                 domain: ZModule | None = None,
                 codomain: ZModule | None = None):

        if not matrix or not matrix[0]:
            raise ValueError(
                "matrix must be a 2d list with at least one entry"
            )

        domain_dimensions = len(matrix[0])

        if any(len(row) != domain_dimensions for row in matrix):
            raise ValueError(
                "All rows of matrix must have equal length"
            )

        if domain and domain_dimensions != domain.dimensions():
            raise ValueError(
                "domain dimension mismatch"
            )

        codomain_dimensions = len(matrix)

        if codomain and codomain_dimensions != codomain.dimensions():
            raise ValueError(
                f"codomain dimension mismatch: " +
                f"expected {codomain.dimensions()}, " +
                f"found {codomain_dimensions}"
            )

        self.domain: ZModule = domain or ZModule.free(domain_dimensions)
        self.codomain: ZModule = codomain or ZModule.free(codomain_dimensions)
        self.matrix: tuple[tuple[int, ...], ...] = tuple(
            tuple(row) for row in matrix[:self.codomain.rank]
        ) + tuple(
            tuple(item % torsion for item in row)
            for (row, torsion)
            in zip(matrix[self.codomain.rank:], self.codomain.torsion_numbers)
        ) or ((0,),)

    @staticmethod
    def zero(domain: ZModule,
             codomain: ZModule) -> Homomorphism:
        return Homomorphism(tuple(
            tuple(0 for _ in range(domain.dimensions()))
            for _ in range(codomain.dimensions())
        ))

    def is_zero(self) -> bool:
        return all(value == 0 for row in self.matrix for value in row)

    @staticmethod
    def identity(module: ZModule) -> Homomorphism:
        return Homomorphism(
            matrix=tuple(tuple(
                1 if row == column else 0
                for column in range(module.dimensions())
            ) for row in range(module.dimensions())),
            domain=module,
            codomain=module
        )

    @staticmethod
    def from_canonical_generator_images(
        images: Sequence[ZModule.Element],
        domain: ZModule | None = None
    ):
        codomain = images[0].module
        if any(image.module.rank != codomain.rank or
               image.module.torsion_numbers != codomain.torsion_numbers
               for image in images):
            raise ValueError("All images must belong to the same module")
        return Homomorphism(([
            tuple(combination_of_coordinates)
            for combination_of_coordinates
            in zip(*(image.coordinates for image in images))
        ]), domain, codomain)

    def apply(
        self,
        element: ZModule.Element
    ) -> ZModule.Element:
        if len(element.coordinates) != self.domain.dimensions():
            raise ValueError("dimension mismatch")
        return self.codomain.element([
            sum(element_coordinate * basis_images
                for (element_coordinate, basis_images) in zip(
                    element.coordinates, row
                ))
            for row in self.matrix])

    def canonical_generator_images(self) -> list[ZModule.Element]:
        return [
            self.codomain.element(column)
            for column in zip(*(self.matrix))
        ]

    def compose(self, other: Homomorphism) -> Homomorphism:
        if (
            self.domain.rank != other.codomain.rank or
            self.domain.torsion_numbers != other.codomain.torsion_numbers
        ):
            raise ValueError("domain and codomain mismatch")

        return Homomorphism(
            matrix=tuple(tuple(
                sum(self.matrix[row_index][k] * other.matrix[k][column_index]
                    for k in range(self.domain.dimensions()))
                for column_index in range(other.domain.dimensions())
            ) for row_index in range(self.codomain.dimensions())),
            domain=other.domain,
            codomain=self.codomain
        )

    def __repr__(self) -> str:
        return (
            f"{self.domain} --> {self.codomain},\n" +
            "\n".join(str(row) for row in self.matrix)
        )

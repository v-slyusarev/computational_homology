from __future__ import annotations
from collections.abc import Sequence

from module_theory.zmodule import ZModule
from module_theory._internal.smith_normal_form import (
    SmithNormalForm, SmithNormalFormCalculator
)
from module_theory._internal.kernel_and_image import KernelAndImageCalculator


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
        ) or (tuple(0 for _ in range(self.domain.dimensions())),)
        self._smith_normal_form: SmithNormalForm | None = None
        self._kernel_generators: tuple[ZModule.Element, ...] | None = None
        if self.domain.is_zero():
            self._kernel_generators = (self.domain.zero_element(),)

    @staticmethod
    def zero(domain: ZModule,
             codomain: ZModule) -> Homomorphism:
        return Homomorphism(tuple(
            tuple(0 for _ in range(domain.dimensions()))
            for _ in range(codomain.dimensions())
        ), domain, codomain)

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
        if not all(image.module.is_identical_to(codomain) for image in images):
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

    def _get_smith_normal_form(self) -> SmithNormalForm:
        if not self._smith_normal_form:
            self._smith_normal_form = (
                SmithNormalFormCalculator(self.matrix).smith_normal_form()
            )
        return self._smith_normal_form

    def preimage(self, element: ZModule.Element) -> ZModule.Element | None:
        if not element.module.is_identical_to(self.codomain):
            raise ValueError(
                "The element must belong to the codomain of the homomorphism"
            )
        # smith_matrix = self._get_smith_normal_form().matrix
        rank = self._get_smith_normal_form().rank
        diagonal_numbers = self._get_smith_normal_form().diagonal[:rank]
        codomain_change_matrix = (self._get_smith_normal_form()
                                      .inverse_row_change_matrix)
        codomain_change_homomorphism = Homomorphism(
            codomain_change_matrix, domain=element.module
        )
        target = codomain_change_homomorphism.apply(element)

        if any(target.coordinates[rank:]):
            return None
        if any(
            coordinate % diagonal_number
            for (coordinate, diagonal_number)
            in zip(target.coordinates, diagonal_numbers)
        ):
            return None

        preimage_changed = self.domain.element([
                coordinate // diagonal_number
                for (coordinate, diagonal_number)
                in zip(target.coordinates, diagonal_numbers)
            ] + [0] * (self.domain.dimensions() - rank)
        )

        domain_change_homomorphism = Homomorphism(
            self._get_smith_normal_form().column_change_matrix,
            domain=self.domain,
            codomain=self.domain
        )

        return domain_change_homomorphism.apply(preimage_changed)

    def kernel_generators(self) -> list[ZModule.Element]:
        if not self._kernel_generators:
            kernel = KernelAndImageCalculator(self.matrix).kernel
            self._kernel_generators = tuple(
                self.domain.element(coordinates_list)
                for coordinates_list in kernel
            )
        return list(self._kernel_generators)

    def __repr__(self) -> str:
        return (
            f"{self.domain} --> {self.codomain},\n" +
            "\n".join(str(row) for row in self.matrix)
        )

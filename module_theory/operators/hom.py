from __future__ import annotations
from collections.abc import Sequence
from typing import Callable
from math import gcd
from module_theory.zmodule import ZModule
from module_theory.cyclic_zmodule import (
    FreeCyclicZModule, TorsionCyclicZModule
)
from module_theory.homomorphism import Homomorphism
from module_theory.operators.direct_sum import direct_sum
from module_theory.operators.cyclic_summands import cyclic_summands
from module_theory.cochain_complex import CochainComplex


class Hom(ZModule):
    def __init__(self, domain: ZModule, codomain: ZModule):
        self.domain: ZModule = domain
        self.codomain: ZModule = codomain
        if self.domain.is_zero() or self.codomain.is_zero():
            super().__init__(0, ())
            self._embeddings: tuple[Homomorphism, ...] = (
                Homomorphism.zero(self.domain, self.codomain),
            )
            return

        sum_of_cyclic, self._embeddings = direct_sum(*(
            self._hom_of_cyclic_modules(domain_summand, codomain_summand)
            for codomain_summand in cyclic_summands(self.codomain)
            for domain_summand in cyclic_summands(self.domain)
        ))

        super().__init__(sum_of_cyclic.rank, sum_of_cyclic.torsion_numbers)
        assert self._embeddings is not None, "_embeddings is None!"

    @staticmethod
    def _hom_of_cyclic_modules(domain: ZModule, codomain: ZModule) -> ZModule:
        # If domain and codomain are cyclic, then find Hom directly:
        match (domain, codomain):
            case (TorsionCyclicZModule(), FreeCyclicZModule()):
                # Hom(Z/pZ, Z) is trivial
                return ZModule.zero()
            case (TorsionCyclicZModule(p), TorsionCyclicZModule(q)):
                # Hom(Z/pZ, Z/qZ) = Z / gcd(p, q)Z
                torsion = gcd(domain.torsion, codomain.torsion)
                if torsion >= 2:
                    return TorsionCyclicZModule(torsion)
                else:
                    return ZModule.zero()
            case (FreeCyclicZModule(), _):
                # Hom(Z, B) is isomorphic to B
                return codomain
            case _:
                raise ValueError(
                    "domain and codomain must be FreeCyclicZModule or " +
                    "TorsionCyclicZModule"
                )

    def element_from_homomorphism(
        self,
        homomorphism: Homomorphism
    ) -> ZModule.Element:
        flattened_matrix = [value
                            for row in homomorphism.matrix
                            for value in row]

        return sum(
            embedding.apply(embedding.domain.element([value]))
            for (value, embedding)
            in zip(flattened_matrix, self._embeddings)
        ) or self.zero_element()

    def homomorphism_from_element(
        self,
        element: ZModule.Element
    ) -> Homomorphism:
        matrix = list(
            list(row) for row
            in Homomorphism.zero(self.domain, self.codomain).matrix
        )

        # List matrix indices that correspond to nontrivial summands
        coordinates_to_matrix_indices = [
            (row_index, column_index)
            for row_index in range(self.codomain.dimensions())
            for column_index in range(self.domain.dimensions())
            if not self._embeddings[
                row_index * self.domain.dimensions() + column_index
            ].is_zero()
        ]

        for (coordinate, (row, column)) in zip(
            element.coordinates, coordinates_to_matrix_indices
        ):
            matrix[row][column] = coordinate

        return Homomorphism(
            matrix, self.domain, self.codomain
        )

    def standard_form(self) -> str:
        return super().__repr__()

    def __repr__(self) -> str:
        return f"Hom({self.domain}, {self.codomain})"


def left_hom(
    cochain_complex: CochainComplex,
    hom_domain: ZModule
) -> CochainComplex:
    hom_modules = [Hom(hom_domain, module) for module in cochain_complex.modules]

    induced_homomorphisms = _calcuate_induced_homomorphisms(
        hom_modules,
        cochain_complex.homomorphisms,
        lambda source_homomorphism, complex_homomorphism: (
            complex_homomorphism.compose(source_homomorphism)
        )
    )

    return CochainComplex(hom_modules, induced_homomorphisms)


def right_hom(
    cochain_complex: CochainComplex,
    hom_codomain: ZModule
) -> CochainComplex:

    hom_modules = [
        Hom(module, hom_codomain) for module in cochain_complex.modules
    ][::-1]

    induced_homomorphisms = _calcuate_induced_homomorphisms(
        hom_modules,
        cochain_complex.homomorphisms[-2::-1],  # invert the order
        lambda source_homomorphism, complex_homomorphism: (
            source_homomorphism.compose(complex_homomorphism)
        )
    )

    return CochainComplex(hom_modules, induced_homomorphisms)


def _calcuate_induced_homomorphisms(
    hom_modules: Sequence[Hom],
    original_homomorphisms: Sequence[Homomorphism],
    homomorphism_mapping: Callable[[Homomorphism, Homomorphism], Homomorphism]
) -> tuple[Homomorphism, ...]:
    induced_homomorphisms: list[Homomorphism] = []

    for (this_hom, next_hom, complex_homomorphism) in zip(
        hom_modules, hom_modules[1:], original_homomorphisms
    ):
        # Calculate the matrices for the images of the canonical generators of
        # Hom(D, C_i) under the action of d_i^*:
        generating_homomorphisms = [
            this_hom.homomorphism_from_element(generator)
            for generator in this_hom.canonical_generators()
        ]

        images_of_generating_homomorphisms = [
            homomorphism_mapping(homomorphism, complex_homomorphism)
            for homomorphism in generating_homomorphisms
        ]

        # Now convert these matrices to their
        # corresponding elements in Hom(D, C_{i+1}):
        images_of_generators = [
            next_hom.element_from_homomorphism(homomorphism)
            for homomorphism in images_of_generating_homomorphisms
        ]

        induced_homomorphism = Homomorphism.from_canonical_generator_images(
            images_of_generators, this_hom
        )

        induced_homomorphisms.append(induced_homomorphism)

    return tuple(induced_homomorphisms)

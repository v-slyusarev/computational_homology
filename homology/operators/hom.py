from __future__ import annotations
from collections.abc import Sequence
from typing import Callable
# from itertools import zip_longest
from math import gcd
from homology.zmodule import ZModule
from homology.cyclic_zmodule import FreeCyclicZModule, TorsionCyclicZModule
from homology.homomorphism import Homomorphism
from homology.operators.direct_sum import direct_sum
from homology.operators.cyclic_summands import cyclic_summands
from homology.chain_complex import ChainComplex


class Hom:
    def __init__(self, domain: ZModule, codomain: ZModule):
        self.domain = domain
        self.codomain = codomain
        self._calculate_hom_module()
        assert self.module is not None, "module is None!"
        assert self._embeddings is not None, "_embeddings is None!"
        self.rank = self.module.rank
        self.torsion_numbers = self.module.torsion_numbers

    def _calculate_hom_module(self):
        if self.domain.is_zero() or self.codomain.is_zero():
            self._set_zero_module()
            return

        # If domain and codomain are cyclic, then find Hom directly:
        if isinstance(self.domain, FreeCyclicZModule):
            if isinstance(self.codomain,
                          (FreeCyclicZModule, TorsionCyclicZModule)):
                # Hom(Z, B) is isomorphic to B
                self._set_cyclic_module(self.codomain)
                return
        elif isinstance(self.domain, TorsionCyclicZModule):
            if isinstance(self.codomain, FreeCyclicZModule):
                # Hom(Z/pZ, Z) is trivial
                self._set_zero_module()
                return
            elif isinstance(self.codomain, TorsionCyclicZModule):
                # Hom(Z/pZ, Z/qZ) = Z / gcd(p, q)Z
                torsion = gcd(self.domain.torsion, self.codomain.torsion)
                if torsion >= 2:
                    self._set_cyclic_module(TorsionCyclicZModule(torsion))
                else:
                    self._set_zero_module()
                return

        self._set_direct_sum_module([
            Hom(domain_summand, codomain_summand).module
            for codomain_summand in cyclic_summands(self.codomain)
            for domain_summand in cyclic_summands(self.domain)
        ])

    def _set_zero_module(self):
        self.module = ZModule.zero()
        self._embeddings = [Homomorphism.zero(self.domain, self.codomain)]

    def _set_cyclic_module(self, module):
        self.module = module
        self._embeddings = [
                Homomorphism([[1]], self.domain, self.codomain)
            ]

    def _set_direct_sum_module(self, modules: Sequence[ZModule]):
        self.module, self._embeddings = direct_sum(*modules)

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
        )

    def homomorphism_from_element(
        self,
        element: ZModule.Element
    ) -> Homomorphism:
        matrix = Homomorphism.zero(self.domain, self.codomain).matrix

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

    def dimensions(self):
        return self.module.dimensions()

    def is_zero(self) -> bool:
        return self.module.is_zero()

    def element(self, coordinates: Sequence[int]) -> ZModule.Element:
        return self.module.element(coordinates)

    def zero_element(self) -> ZModule.Element:
        return self.module.zero_element()

    def canonical_generators(self) -> list[ZModule.Element]:
        return self.module.canonical_generators()

    def standard_form(self) -> str:
        return str(self.module)

    def __repr__(self) -> str:
        return f"Hom({self.domain}, {self.codomain})"


def left_hom(
    chain_complex: ChainComplex,
    hom_domain: ZModule
) -> ChainComplex:
    hom_modules = [Hom(hom_domain, module) for module in chain_complex.modules]

    induced_homomorphisms = _calcuate_induced_homomorphisms(
        hom_modules,
        chain_complex.homomorphisms,
        lambda source_homomorphism, complex_homomorphism: (
            complex_homomorphism.compose(source_homomorphism)
        )
    )

    return ChainComplex(hom_modules, induced_homomorphisms)


def right_hom(
    chain_complex: ChainComplex,
    hom_codomain: ZModule
) -> ChainComplex:

    hom_modules = [
        Hom(module, hom_codomain) for module in chain_complex.modules
    ][::-1]

    induced_homomorphisms = _calcuate_induced_homomorphisms(
        hom_modules,
        chain_complex.homomorphisms[-2::-1],  # invert the order
        lambda source_homomorphism, complex_homomorphism: (
            source_homomorphism.compose(complex_homomorphism)
        )
    )

    return ChainComplex(hom_modules, induced_homomorphisms)


def _calcuate_induced_homomorphisms(
    hom_modules: Sequence[Hom],
    original_homomorphisms: Sequence[Homomorphism],
    homomorphism_mapping: Callable[[Homomorphism, Homomorphism], Homomorphism]
) -> Sequence[Homomorphism]:
    induced_homomorphisms = []

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

        # Now convert these matrices to the canonical coordinates of their
        # respective elements in Hom(D, C_{i+1}):
        images_of_generators_coordinates = [
            next_hom.element_from_homomorphism(homomorphism).coordinates
            for homomorphism in images_of_generating_homomorphisms
        ]

        # The columns of the matrix for d_i^* are the coordinates of the
        # images of the canonical generators of C_i:
        induced_homomorphism_matrix = [
            list(coordinates_for_generator)
            for coordinates_for_generator
            in zip(*images_of_generators_coordinates)
        ]

        induced_homomorphism = Homomorphism(
            matrix=induced_homomorphism_matrix,
            domain=this_hom,
            codomain=next_hom
        )

        induced_homomorphisms.append(induced_homomorphism)

    return induced_homomorphisms

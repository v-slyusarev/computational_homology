from __future__ import annotations
from collections.abc import Sequence
from typing import Callable
from math import gcd
from homology.zmodule import FinitelyGeneratedZModule
from homology.operators.direct_sum import direct_sum


def hom(domain: FinitelyGeneratedZModule,
        codomain: FinitelyGeneratedZModule) -> (
            FinitelyGeneratedZModule,
            Callable[
                Sequence[Sequence[int]],
                FinitelyGeneratedZModule.Element
            ],
            Callable[
                Sequence[Sequence[int]],
                FinitelyGeneratedZModule.Element
            ]
        ):

    if domain.is_zero() or codomain.is_zero():
        hom_module = FinitelyGeneratedZModule.zero()
        return hom_module, lambda _: hom_module.zero_element(), lambda _: [[0]]

    # Represent the Hom as a direct sum of cyclic modules that correspond
    # to maps from domain's basis elements to codomain's basis elements

    # Hom(Z, Z) = Z
    Z_to_Z_summands = [FinitelyGeneratedZModule.free(1)] * domain.rank

    #  Hom(Z / qZ, Z) = 0
    torsion_to_Z_summands = [
            FinitelyGeneratedZModule.zero() for _ in domain.torsion_numbers
        ]

    # Repeat this for all Z summands of codomain
    to_Z_summands = ((Z_to_Z_summands + torsion_to_Z_summands)
                     * codomain.rank)

    to_torsion_summands = []

    for q in codomain.torsion_numbers:
        # Hom(Z, Z / qZ) = Z/ qZ
        Z_to_torsion_summands = ([FinitelyGeneratedZModule(0, [q])]
                                 * domain.rank)
        to_torsion_summands += Z_to_torsion_summands

        # Hom(Z / pZ, Z / qZ) = Z / gcd(p, q) Z
        torsion_to_torsion_summands = []
        for p in domain.torsion_numbers:
            hom_torsion = gcd(p, q)
            if gcd(p, q) >= 2:
                torsion_to_torsion_summands.append(
                    FinitelyGeneratedZModule(0, [hom_torsion])
                )
            else:
                torsion_to_torsion_summands.append(
                    FinitelyGeneratedZModule.zero()
                )
        to_torsion_summands += torsion_to_torsion_summands

    summands = to_Z_summands + to_torsion_summands

    hom_module, embeddings = direct_sum(summands)

    def matrix_to_hom(matrix: Sequence[Sequence[int]]):
        flattened_matrix = [value for row in matrix for value in row]
        pass

    def hom_to_matrix(element: FinitelyGeneratedZModule.Element):
        pass

    return hom_module, matrix_to_hom, hom_to_matrix

    # return FinitelyGeneratedZModule(
    #     domain.rank * codomain.rank,
    #     codomain.torsion_numbers * domain.rank + [
    #         gcd(p, q)
    #         for p in domain.torsion_numbers
    #         for q in codomain.torsion_numbers
    #         if gcd(p, q) > 1
    #     ]
    # )

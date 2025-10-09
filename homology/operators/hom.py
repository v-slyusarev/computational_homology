from __future__ import annotations
from collections.abc import Sequence
from typing import Callable
from math import gcd
from homology.homomorphism import Homomorphism
from homology.zmodule import ZModule
from homology.operators.direct_sum import direct_sum
from homology.chain_complex import ChainComplex


def hom(domain: ZModule, codomain: ZModule) -> (
            ZModule,
            Callable[Sequence[Sequence[int]], ZModule.Element],
            Callable[ZModule.Element, Sequence[Sequence[int]]]
        ):

    if domain.is_zero() or codomain.is_zero():
        hom_module = ZModule.zero()
        return hom_module, lambda _: hom_module.zero_element(), lambda _: [[0]]

    coordinates_to_matrix = []

    # Represent the Hom as a direct sum of cyclic modules that correspond
    # to maps from domain's basis elements to codomain's basis elements

    # Hom(Z, Z) = Z
    Z_to_Z_summands = [ZModule.free(1)] * domain.rank

    #  Hom(Z / qZ, Z) = 0
    torsion_to_Z_summands = [
            ZModule.zero() for _ in domain.torsion_numbers
        ]

    # Repeat this for all Z summands of codomain
    to_Z_summands = ((Z_to_Z_summands + torsion_to_Z_summands)
                     * codomain.rank)
    coordinates_to_matrix += [(row, column)
                              for row in range(codomain.rank)
                              for column in range(domain.rank)]

    to_torsion_summands = []

    for q_index, q in enumerate(codomain.torsion_numbers):
        row = codomain.rank + q_index
        # Hom(Z, Z / qZ) = Z/ qZ
        Z_to_torsion_summands = ([ZModule(0, [q])] * domain.rank)
        to_torsion_summands += Z_to_torsion_summands
        coordinates_to_matrix += [(row, column)
                                  for column in range(domain.rank)]

        # Hom(Z / pZ, Z / qZ) = Z / gcd(p, q) Z
        torsion_to_torsion_summands = []
        for p_index, p in enumerate(domain.torsion_numbers):
            column = domain.rank + p_index
            hom_torsion = gcd(p, q)
            if gcd(p, q) >= 2:
                torsion_to_torsion_summands.append(ZModule(0, [hom_torsion]))
                coordinates_to_matrix.append((row, column))
            else:
                torsion_to_torsion_summands.append(
                    ZModule.zero()
                )
        to_torsion_summands += torsion_to_torsion_summands

    summands = to_Z_summands + to_torsion_summands

    hom_module, embeddings = direct_sum(summands)

    # Given a matrix of a homomorphism, returns a list of its canonical
    # coordinates in the Hom module.
    def matrix_to_hom(matrix: Sequence[Sequence[int]]):
        flattened_matrix = [value for row in matrix for value in row]

        return sum(
            embedding.apply(summand.element([value]))
            for (value, summand, embedding)
            in zip(flattened_matrix, summands, embeddings)
        )

    # Given an element of the Hom module represented with its
    # canonical coordinates, returns a matrix of the corresponding
    # homomorphism with respect to the canonical coordinates
    # of its domain and codomain
    def hom_to_matrix(element: ZModule.Element):
        matrix = Homomorphism.zero(domain, codomain).matrix
        for (coordinate, (row, column)) in zip(element.coordinates,
                                               coordinates_to_matrix):
            matrix[row][column] = coordinate
        return matrix

    return hom_module, matrix_to_hom, hom_to_matrix


def left_hom(chain_complex: ChainComplex, hom_domain: ZModule) -> ChainComplex:
    hom_modules_with_functions = [
        hom(hom_domain, complex_module)
        for complex_module in chain_complex.modules
    ]
    hom_modules = [hom_module
                   for (hom_module, _, _) in hom_modules_with_functions]

    hom_homomorphisms = []

    # Iterate over the pairs of modules Hom(D, C_i) --d_i^*--> Hom(D, C_{i+1})
    # to calculate the matrices of d_i^*
    for ((this_hom_module, _, this_hom_to_matrix),
         (next_hom_module, next_matrix_to_hom, _),
         complex_homomorphism) in zip(hom_modules_with_functions,
                                      hom_modules_with_functions[1:],
                                      chain_complex.homomorphisms):

        # Calculate the matrices for the images of the canonical generators of
        # Hom(D, C_i) under the action of d_i^*:
        generators_matrices = [this_hom_to_matrix(generator)
                               for generator
                               in this_hom_module.canonical_generators()]

        images_of_generators_matrices = [
            complex_homomorphism.compose(
                Homomorphism(generator_matrix, hom_domain, next_hom_module)
            ).matrix for generator_matrix in generators_matrices
        ]

        # Now convert these matrices to the canonical coordinates of their
        # respective elements in Hom(D, C_{i+1}):
        images_of_generators_coordinates = [
            next_matrix_to_hom(image_matrix).coordinates
            for image_matrix in images_of_generators_matrices
        ]

        # The columns of the matrix for d_i^* are the coordinates of the
        # images of the canonical generators of C_i:
        hom_homomorphism_matrix = [list(coordinates_for_generator)
                                   for coordinates_for_generator
                                   in zip(*images_of_generators_coordinates)]

        hom_homomorphisms.append(Homomorphism(
            matrix=hom_homomorphism_matrix,
            domain=this_hom_module,
            codomain=next_hom_module
        ))

    return ChainComplex(hom_modules, hom_homomorphisms)

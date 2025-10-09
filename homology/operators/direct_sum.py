from __future__ import annotations
from collections.abc import Sequence
from homology.zmodule import ZModule
from homology.homomorphism import Homomorphism


def direct_sum(modules: Sequence[ZModule]) -> (ZModule,
                                               Sequence[Homomorphism]):

    direct_sum_module = ZModule(
        rank=sum(module.rank for module in modules),
        torsion_numbers=[factor for module in modules
                         for factor in module.torsion_numbers]
     )

    embeddings = []
    free_part_position = 0
    torsion_part_position = 0

    for module in modules:
        embedding_matrix = Homomorphism.zero(module, direct_sum_module).matrix

        for i in range(module.rank):
            embedding_matrix[free_part_position + i][i] = 1
        free_part_position += module.rank

        for i in range(len(module.torsion_numbers)):
            embedding_matrix[direct_sum_module.rank +
                             torsion_part_position + i][module.rank + i] = 1
        torsion_part_position += len(module.torsion_numbers)

        embeddings.append(
            Homomorphism(embedding_matrix, module, direct_sum_module)
        )

    return direct_sum_module, embeddings

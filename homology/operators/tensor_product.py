from collections.abc import Sequence
import itertools
import math
from homology.zmodule import ZModule
from homology.cyclic_zmodule import *
from homology.operators.cyclic_summands import cyclic_summands
from homology.operators.direct_sum import direct_sum


TENSOR_PRODUCT_SEPARATOR_SYMBOL = " ⊗ "


class TensorProduct:
    def __init__(self, *multipliers: ZModule):
        if len(multipliers) < 2:
            raise ValueError("At least 2 tensor multipliers must be provided")
        self.multipliers = multipliers
        self._calculate_tensor_product()
        assert self.module is not None, "module is None!"
        assert self._embeddings is not None, "_embeddings is None!"
        self.rank = self.module.rank
        self.torsion_numbers = self.module.torsion_numbers

    def _calculate_tensor_product(self):
        cyclic_summand_representations = [
            cyclic_summands(module) for module in self.multipliers
        ]

        cyclic_mutiplier_combinations = [*itertools.product(
            *cyclic_summand_representations
        )]

        direct_summands = [
            self._tensor_product_of_cyclic_modules(combination)
            for combination in cyclic_mutiplier_combinations
        ]

        self.module, self._embeddings = direct_sum(*direct_summands)

    @staticmethod
    def _tensor_product_of_cyclic_modules(modules: ZModule) -> ZModule:
        if any(module.is_zero() for module in modules):
            return ZModule.zero()

        rank = int(any(module.rank for module in modules))
        torsion_numbers = [
            number for module in modules for number in module.torsion_numbers
        ]
        if not torsion_numbers:
            return ZModule.free(rank)

        torsion = math.gcd(*torsion_numbers)

        if torsion >= 2:
            return TorsionCyclicZModule(torsion)
        else:
            return ZModule.zero()

    def pure_tensor(self, *multipliers: ZModule.Element) -> ZModule.Element:
        if len(multipliers) != len(self.multipliers):
            raise ValueError("Mismatch in number of tensor multipliers")

        combinations = [*itertools.product(
            *(element.coordinates for element in multipliers)
        )]
        direct_summands = cyclic_summands(self)

        summand_elements = [
            summand.element([math.prod(combination)])
            for (combination, summand) in zip(combinations, direct_summands)
        ]

        return sum(
            embedding.apply(summand_element)
            for (embedding, summand_element)
            in zip(self._embeddings, summand_elements)
        )

    def dimensions(self) -> int:
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
        return TENSOR_PRODUCT_SEPARATOR_SYMBOL.join(
            f"({module})" if module.dimensions() > 1 else str(module)
            for module in self.multipliers
        )

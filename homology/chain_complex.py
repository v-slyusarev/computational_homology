from __future__ import annotations
from collections.abc import Sequence
from homology.zmodule import ZModule
from homology.homomorphism import Homomorphism

ARROW_START_SYMBOL = " --"
ARROW_END_SYMBOL = "--> "
HOMOMORPHISM_SYMBOL = "d"


class ChainComplex:
    def __init__(self,
                 modules: Sequence[ZModule],
                 homomorphisms: Sequence[Homomorphism]):
        if not modules:
            raise ValueError("modules must be non-empty")

        if homomorphisms is None:
            homomorphisms = ()

        if len(homomorphisms) == len(modules) - 1:
            homomorphisms = [*homomorphisms, Homomorphism.zero(
                modules[-1], ZModule.zero()
            )]

        if len(modules) != len(homomorphisms):
            raise ValueError("modules and homomorphisms length mismatch")

        self.modules = modules
        self.homomorphisms = homomorphisms

    @staticmethod
    def __arrow(index: int) -> str:
        return (ARROW_START_SYMBOL
                + HOMOMORPHISM_SYMBOL
                + str(index)
                + ARROW_END_SYMBOL)

    def __repr__(self) -> str:
        repr_string = "0" + self.__arrow(0)
        for index, module in enumerate(self.modules):
            repr_string += str(module)
            repr_string += self.__arrow(index + 1)
        repr_string += "0"
        return repr_string

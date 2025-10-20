from __future__ import annotations
from collections.abc import Sequence
from module_theory.zmodule import ZModule
from module_theory.homomorphism import Homomorphism

ARROW_START_SYMBOL = " --"
ARROW_END_SYMBOL = "--> "
HOMOMORPHISM_SYMBOL = "d"


class CochainComplex:
    def __init__(self,
                 modules: Sequence[ZModule],
                 homomorphisms: Sequence[Homomorphism]):
        if not modules:
            raise ValueError("modules must be non-empty")

        if len(homomorphisms) == len(modules) - 1:
            homomorphisms = [*homomorphisms, Homomorphism.zero(
                modules[-1], ZModule.zero()
            )]

        if len(modules) != len(homomorphisms):
            raise ValueError("modules and homomorphisms length mismatch")

        self.modules: tuple[ZModule, ...] = tuple(modules)
        self.homomorphisms: tuple[Homomorphism, ...] = tuple(homomorphisms)

    def left_pad(self, count: int = 1) -> CochainComplex:
        zero = ZModule.zero()
        return CochainComplex(
            modules=(zero,) * count + self.modules,
            homomorphisms=(Homomorphism.zero(zero, zero),) * (count - 1) +
            (Homomorphism.zero(zero, self.modules[0]),) + self.homomorphisms
        )

    def right_pad(self, count: int = 1) -> CochainComplex:
        zero = ZModule.zero()
        return CochainComplex(
            modules=self.modules + (zero,) * count,
            homomorphisms=self.homomorphisms
            + (Homomorphism.zero(self.modules[-1], zero),)
            + (Homomorphism.zero(zero, zero),) * (count - 1)
        )

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
        repr_string += "\n"
        for index, homomorphism in enumerate(self.homomorphisms):
            repr_string += f"{HOMOMORPHISM_SYMBOL}{index+1}: {homomorphism}\n"
        return repr_string

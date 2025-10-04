from collections.abc import Sequence

DIRECT_SUM_SEPARATOR_SYMBOL = " ⊕ "
Z_SYMBOL = "ℤ"
POWER_SYMBOL = "^"
QUOTIENT_SYMBOL = "/"


class FinitelyGeneratedZModule:
    def __init__(self,
                 rank: int,
                 betti_numbers: Sequence[int]):
        if rank < 0:
            raise ValueError("rank must be non-negative")
        # if rank == 0 and not betti_numbers:
        #     raise ValueError("for rank == 0 betti_numbers must be non-empty")
        if any(value < 2 for value in betti_numbers):
            raise ValueError("every Betti number must be at least 2")

        self.rank = rank
        self.betti_numbers = betti_numbers

    def dimensions(self):
        return max(self.rank + len(self.betti_numbers), 1)

    def __repr__(self) -> str:
        free_part = None
        torsion_part = None

        if self.rank > 0:
            free_part = self.__free_module_repr(self.rank)

        if self.betti_numbers:
            torsion_part = self.__torsion_module_repr(self.betti_numbers)

        repr_string = DIRECT_SUM_SEPARATOR_SYMBOL.join(
            x for x in (free_part, torsion_part) if x is not None
        )

        if repr_string:
            return repr_string
        else:
            return "0"

    @staticmethod
    def __free_module_repr(rank: int) -> str:
        repr_string = Z_SYMBOL
        if rank > 1:
            repr_string += POWER_SYMBOL + str(rank)
        return repr_string

    @staticmethod
    def __quotient_module_repr(torsion_coefficient: int) -> str:
        return Z_SYMBOL + QUOTIENT_SYMBOL + str(torsion_coefficient) + Z_SYMBOL

    @staticmethod
    def __torsion_module_repr(betti_numbers: Sequence[int]) -> str:
        return DIRECT_SUM_SEPARATOR_SYMBOL.join(
            FinitelyGeneratedZModule.__quotient_module_repr(value)
            for value in betti_numbers
        )


def zero_module():
    return FinitelyGeneratedZModule(0, [])


def free_Z_module(rank: int):
    return FinitelyGeneratedZModule(rank, [])

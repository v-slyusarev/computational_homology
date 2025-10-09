from __future__ import annotations
from collections.abc import Sequence

DIRECT_SUM_SEPARATOR_SYMBOL = " ⊕ "
Z_SYMBOL = "ℤ"
POWER_SYMBOL = "^"
QUOTIENT_SYMBOL = "/"
IDEAL_SEPARATOR_SYMBOL = " + "
COORDINATE_SEPARATOR_SYMBOL = ", "


class FinitelyGeneratedZModule:
    def __init__(self,
                 rank: int,
                 torsion_numbers: Sequence[int]):
        if rank < 0:
            raise ValueError("rank must be non-negative")
        if any(value < 2 for value in torsion_numbers):
            raise ValueError("every Betti number must be at least 2")

        self.rank = rank
        self.torsion_numbers = torsion_numbers

    @staticmethod
    def zero() -> FinitelyGeneratedZModule:
        return FinitelyGeneratedZModule(0, [])

    @staticmethod
    def free(rank: int) -> FinitelyGeneratedZModule:
        return FinitelyGeneratedZModule(rank, [])

    def dimensions(self) -> int:
        return max(self.rank + len(self.torsion_numbers), 1)

    def is_zero(self) -> bool:
        return self.rank == 0 and not self.torsion_numbers

    def element(
        self,
        coordinates: Sequence[int]
    ) -> FinitelyGeneratedZModule.Element:
        return FinitelyGeneratedZModule.Element(self, coordinates)

    def zero_element(self) -> FinitelyGeneratedZModule.Element:
        return self.element([0 for _ in range(self.dimensions())])

    def canonical_generators(self) -> list[FinitelyGeneratedZModule.Element]:
        if self.is_zero():
            return [self.zero_element()]

        return [self.element([1 if coordinate == generator_index else 0
                              for coordinate in range(self.dimensions())])
                for generator_index in range(self.dimensions())]

    def __repr__(self) -> str:
        free_part = None
        torsion_part = None

        if self.rank > 0:
            free_part = self.__free_module_repr(self.rank)

        if self.torsion_numbers:
            torsion_part = self.__torsion_module_repr(self.torsion_numbers)

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
    def __torsion_module_repr(torsion_numbers: Sequence[int]) -> str:
        return DIRECT_SUM_SEPARATOR_SYMBOL.join(
            FinitelyGeneratedZModule.__quotient_module_repr(value)
            for value in torsion_numbers
        )

    class Element:
        def __init__(self,
                     module: FinitelyGeneratedZModule,
                     coordinates: Sequence[int]):

            if module is None or coordinates is None:
                raise ValueError("arguments must not be None")

            if len(coordinates) != module.dimensions():
                raise ValueError("length of coordinates must be equal to the "
                                 "number of dimensions in module")

            self.module = module
            self.coordinates = coordinates

        def __add__(
            self,
            other: FinitelyGeneratedZModule.Element
        ) -> FinitelyGeneratedZModule.Element:
            if (
                self.module.rank != other.module.rank or
                self.module.torsion_numbers != other.module.torsion_numbers
            ):
                raise ValueError("Summands must belong to the same module")

            return self.module.element([
                left_summand_coordinate + right_summand_coordinate
                for (left_summand_coordinate, right_summand_coordinate)
                in zip(self.coordinates, other.coordinates)
            ])

        def __radd__(
            self,
            other: FinitelyGeneratedZModule.Element
        ) -> FinitelyGeneratedZModule.Element:
            if other is not FinitelyGeneratedZModule.Element:
                return self

            return self + other

        def __repr__(self) -> str:
            if self.module.is_zero():
                return "0"

            normalized_coordinates = []
            torsion_coordinates = []

            if self.module.rank > 0:
                normalized_coordinates += (
                    str(value) for value in self.coordinates[:self.module.rank]
                )
                torsion_coordinates = self.coordinates[self.module.rank:]
            else:
                torsion_coordinates = self.coordinates

            normalized_coordinates += [
                str(value % invariant_factor)
                + self.__ideal_repr(invariant_factor)
                for (value, invariant_factor)
                in zip(torsion_coordinates, self.module.torsion_numbers)
            ]
            repr_string = COORDINATE_SEPARATOR_SYMBOL.join(
                normalized_coordinates
            )

            if len(self.coordinates) > 1:
                repr_string = "(" + repr_string + ")"

            return repr_string

        @staticmethod
        def __ideal_repr(invariant_factor: int) -> str:
            return IDEAL_SEPARATOR_SYMBOL + str(invariant_factor) + Z_SYMBOL

from __future__ import annotations
from collections.abc import Sequence

DIRECT_SUM_SEPARATOR_SYMBOL = " ⊕ "
Z_SYMBOL = "ℤ"
POWER_SYMBOL = "^"
QUOTIENT_SYMBOL = "/"
IDEAL_SEPARATOR_SYMBOL = " + "
COORDINATE_SEPARATOR_SYMBOL = ", "


class ZModule:
    def __init__(self,
                 rank: int,
                 torsion_numbers: Sequence[int]):
        if rank < 0:
            raise ValueError("rank must be non-negative")
        if any(value < 2 for value in torsion_numbers):
            raise ValueError("every Betti number must be at least 2")

        self.rank: int = rank
        self.torsion_numbers: tuple[int, ...] = tuple(torsion_numbers)

    @staticmethod
    def zero() -> ZModule:
        return ZModule(0, ())

    @staticmethod
    def free(rank: int) -> ZModule:
        return ZModule(rank, ())

    def dimensions(self) -> int:
        return max(self.rank + len(self.torsion_numbers), 1)

    def is_zero(self) -> bool:
        return self.rank == 0 and not self.torsion_numbers

    def is_identical_to(self, other: ZModule) -> bool:
        return (self.rank == other.rank
                and self.torsion_numbers == other.torsion_numbers)

    def element(self, coordinates: Sequence[int]) -> ZModule.Element:
        return ZModule.Element(self, coordinates)

    def zero_element(self) -> ZModule.Element:
        return self.element([0 for _ in range(self.dimensions())])

    def canonical_generators(self) -> list[ZModule.Element]:
        if self.is_zero():
            return [self.zero_element()]

        return [
            self.element([
                1 if coordinate == generator_index else 0
                for coordinate in range(self.dimensions())
            ]) for generator_index in range(self.dimensions())
        ]

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
            ZModule.__quotient_module_repr(value)
            for value in torsion_numbers
        )

    class Element:
        def __init__(self, module: ZModule, coordinates: Sequence[int]):
            if len(coordinates) != module.dimensions():
                print("ERROR:")
                print(coordinates)
                print(module)
                raise ValueError("length of coordinates must be equal to " +
                                 "the number of dimensions in module")

            self.module: ZModule = module
            if self.module.is_zero():
                self.coordinates: tuple[int, ...] = (0,)
            else:
                self.coordinates = tuple(
                    coordinates[:module.rank]
                ) + tuple(
                    coordinate % torsion for (coordinate, torsion) in zip(
                        coordinates[module.rank:], module.torsion_numbers
                    )
                )

        def is_zero(self) -> bool:
            return not any(self.coordinates)

        def __add__(self, other: ZModule.Element) -> ZModule.Element:
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

        def __radd__(self, other: object) -> ZModule.Element:
            if isinstance(other, ZModule.Element):
                return self + other
            else:
                return self

        def __repr__(self) -> str:
            if self.module.is_zero():
                return "0"

            string_coordinates = [
                str(value) for value in self.coordinates[:self.module.rank]
            ] + [
                str(value) + self.__ideal_repr(torsion_number)
                for (value, torsion_number) in zip(
                    self.coordinates[self.module.rank:],
                    self.module.torsion_numbers
                )
            ]

            repr_string = COORDINATE_SEPARATOR_SYMBOL.join(
                string_coordinates
            )

            if len(self.coordinates) > 1:
                repr_string = "(" + repr_string + ")"

            return repr_string

        @staticmethod
        def __ideal_repr(torsion_number: int) -> str:
            return IDEAL_SEPARATOR_SYMBOL + str(torsion_number) + Z_SYMBOL

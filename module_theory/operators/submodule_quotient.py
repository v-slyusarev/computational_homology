from typing import Any


from collections.abc import Sequence
from module_theory.zmodule import ZModule
from module_theory.homomorphism import Homomorphism
from module_theory._internal.smith_normal_form import SmithNormalFormCalculator
from module_theory._internal.reduction import reduction
import itertools


class SubmoduleQuotient(ZModule):
    def __init__(self,
                 generators: Sequence[ZModule.Element],
                 kernel_generators: Sequence[ZModule.Element]):
        print("SubmoduleQuotient")
        print(generators)
        print(kernel_generators)

        generators = reduction(generators)

        if all(generator.is_zero() for generator in generators):
            super().__init__(0, ())
            return

        self.original_module = generators[0].module

        if not all(generator.module.is_identical_to(self.original_module)
                   for generator in generators):
            raise ValueError("All generators must be from the same module")

        projection_to_generators = (
            Homomorphism.from_canonical_generator_images(generators)
        )

        preimages = [projection_to_generators.domain.zero_element()]
        for kernel_generator in kernel_generators:
            preimage = projection_to_generators.preimage(kernel_generator)
            if preimage is None:
                raise ValueError(
                    "images of generators do not span kernel_generators"
                )
            preimages.append(preimage)

        projection_to_preimages = (
            Homomorphism.from_canonical_generator_images(preimages)
        )

        smith_normal_form = SmithNormalFormCalculator(
            projection_to_preimages.matrix
        ).smith_normal_form()

        change_matrix = Homomorphism(
            smith_normal_form.inverse_row_change_matrix
        )

        self.quotient_generators = (
            projection_to_generators.compose(change_matrix)
                                    .canonical_generator_images()
        )

        orders_of_generators = [
            generator.order() for generator in self.quotient_generators
        ]
        print("smith_normal_form.diagonal")
        print(smith_normal_form.diagonal[:smith_normal_form.rank])
        print("orders_of_generators")
        print(orders_of_generators)

        rank = 0
        torsion_numbers: list[int] = []
        for (generator_order, quotient_torsion) in itertools.zip_longest(
            orders_of_generators,
            smith_normal_form.diagonal[:smith_normal_form.rank]
        ):
            # First branch: this element spans some kernel generator
            if quotient_torsion:
                # Add if it spans a multiple of that generator,
                # Otherwise it is killed off: do nothing
                if quotient_torsion >= 2:
                    torsion_numbers.append(quotient_torsion)
            # Second branch: this element spans no kernel generator
            # If this element is torsion-free, it contributes to the rank
            elif not generator_order:
                rank += 1
            # Otherwise it contributes to the torsion
            else:
                torsion_numbers.append(generator_order)

        print(rank, torsion_numbers)
        super().__init__(rank, torsion_numbers)


class Submodule(SubmoduleQuotient):
    def __init__(self, generators: Sequence[ZModule.Element]):
        super().__init__(generators, [])


class Quotient(SubmoduleQuotient):
    def __init__(
        self, module: ZModule, kernel_generators: Sequence[ZModule.Element]
    ):
        super().__init__(module.canonical_generators(), kernel_generators)

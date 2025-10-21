from collections.abc import Sequence
from module_theory.zmodule import ZModule
from module_theory.homomorphism import Homomorphism
from module_theory._internal.smith_normal_form import SmithNormalFormCalculator


class SubmoduleQuotient(ZModule):
    def __init__(self,
                 generators: Sequence[ZModule.Element],
                 kernel_generators: Sequence[ZModule.Element]):

        if not generators:
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

        torsions = smith_normal_form.diagonal[:smith_normal_form.rank]
        rank = len(generators) - len(torsions)

        super().__init__(
            rank, [torsion for torsion in torsions if torsion > 1]
        )

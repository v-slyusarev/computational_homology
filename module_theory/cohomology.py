from module_theory.zmodule import ZModule
from module_theory.cochain_complex import CochainComplex
from module_theory.operators.submodule_quotient import SubmoduleQuotient


def cohomology(cochain_complex: CochainComplex) -> list[ZModule]:
    kernel_generator_sets: list[list[ZModule.Element]] = []
    image_generator_sets: list[list[ZModule.Element]] = [[]]

    for homomorphism in cochain_complex.homomorphisms:
        kernel_generator_sets.append(homomorphism.kernel_generators())
        image_generator_sets.append(homomorphism.canonical_generator_images())

    return [
        SubmoduleQuotient(kernel_generator_set, image_generator_set)
        for kernel_generator_set, image_generator_set
        in zip(kernel_generator_sets, image_generator_sets)
    ]

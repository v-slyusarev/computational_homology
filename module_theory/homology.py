from module_theory.zmodule import ZModule
from module_theory.cochain_complex import CochainComplex
from module_theory.operators.submodule_quotient import SubmoduleQuotient


def homology(cochain_complex: CochainComplex) -> list[ZModule]:
    kernel_generator_sets: list[list[ZModule.Element]] = []
    image_generator_sets: list[list[ZModule.Element]] = []

    cochain_complex = cochain_complex.left_pad()
    # print()
    # print(cochain_complex)

    for homomorphism in cochain_complex.homomorphisms:
        kernel_generator_sets.append(homomorphism.kernel_generators())
        image_generator_sets.append(homomorphism.canonical_generator_images())

    # print("kernel_generator_sets", kernel_generator_sets)
    # print("image_generator_sets", image_generator_sets)

    # for d_i, d_i_plus_one, kernel_generator_set, image_generator_set in zip(
    #     cochain_complex.homomorphisms[1:], cochain_complex.homomorphisms,
    #     kernel_generator_sets[1:], image_generator_sets
    # ):
    #     print("LOOP")
    #     print("kernel of")
    #     print(d_i)
    #     print("over the image of")
    #     print(d_i_plus_one)
    #     result.append(
    #         SubmoduleQuotient(kernel_generator_set, image_generator_set)
    #     )

    return [
        SubmoduleQuotient(kernel_generator_set, image_generator_set)
        for kernel_generator_set, image_generator_set
        in zip(kernel_generator_sets[1:], image_generator_sets)
    ]

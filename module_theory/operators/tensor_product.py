from collections.abc import Sequence
import itertools
import math
from module_theory.zmodule import ZModule
from module_theory.homomorphism import Homomorphism
from module_theory.cochain_complex import CochainComplex
from module_theory.cyclic_zmodule import *
from module_theory.operators.cyclic_summands import cyclic_summands
from module_theory.operators.direct_sum import direct_sum


TENSOR_PRODUCT_SEPARATOR_SYMBOL = " ⊗ "


class TensorProduct(ZModule):
    def __init__(self, *multipliers: ZModule):
        if len(multipliers) < 2:
            raise ValueError("At least 2 tensor multipliers must be provided")
        self.multipliers: tuple[ZModule, ...] = multipliers
        module, embeddings = self._calculate_tensor_product()
        super().__init__(module.rank, module.torsion_numbers)
        self._embeddings: tuple[Homomorphism, ...] = embeddings

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

        return direct_sum(*direct_summands)

    @staticmethod
    def _tensor_product_of_cyclic_modules(
        modules: Sequence[ZModule]
    ) -> ZModule:
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
        ) or self.zero_element()

    def homomorphism(self, *components: Homomorphism) -> Homomorphism:
        if not all(
            component.domain.is_identical_to(multiplier)
            for (component, multiplier)
            in zip(components, self.multipliers)
        ):
            raise ValueError("Mismatch in number of components")

        component_codomains = [
            component.codomain for component in components
        ]

        codomain = TensorProduct(*component_codomains)

        canonical_generator_images: list[TensorProduct.Element] = [
            codomain.pure_tensor(*(image_combination))
            for image_combination, embedding in zip(
                itertools.product(*(component.canonical_generator_images()
                                    for component in components)),
                self._embeddings
            )
            if not embedding.is_zero()
        ]

        return Homomorphism.from_canonical_generator_images(
            canonical_generator_images, self
        )

    def standard_form(self) -> str:
        return super().__repr__()

    def __repr__(self) -> str:
        return TENSOR_PRODUCT_SEPARATOR_SYMBOL.join(
            f"({module})" if module.dimensions() > 1 else str(module)
            for module in self.multipliers
        )


def left_tensor_product(
    cochain_complex: CochainComplex,
    multiplier: ZModule
) -> CochainComplex:
    tensor_products = [
            TensorProduct(multiplier, module)
            for module in cochain_complex.modules
        ]
    tensor_homomorphisms = [
        tensor_product.homomorphism(
            Homomorphism.identity(multiplier), complex_homomorphism
        ) for (tensor_product, complex_homomorphism)
        in zip(tensor_products, cochain_complex.homomorphisms)
    ]
    return CochainComplex(tensor_products, tensor_homomorphisms)


def right_tensor_product(
    cochain_complex: CochainComplex,
    multiplier: ZModule
) -> CochainComplex:
    tensor_products = [
            TensorProduct(module, multiplier)
            for module in cochain_complex.modules
        ]
    tensor_homomorphisms = [
        tensor_product.homomorphism(
            complex_homomorphism, Homomorphism.identity(multiplier)
        ) for (tensor_product, complex_homomorphism)
        in zip(tensor_products, cochain_complex.homomorphisms)
    ]
    return CochainComplex(tensor_products, tensor_homomorphisms)

import unittest
from module_theory.zmodule import ZModule
from module_theory.homomorphism import Homomorphism


class TestHomomorphism(unittest.TestCase):
    def test_zero(self):
        A = ZModule(2, [])
        B = ZModule(3, [])
        zero = Homomorphism.zero(A, B)
        self.assertEqual(
            zero.matrix,
            ((0, 0),
             (0, 0),
             (0, 0))
        )
        self.assertEqual(zero.domain.rank, 2)
        self.assertEqual(zero.domain.torsion_numbers, ())
        self.assertEqual(zero.codomain.rank, 3)
        self.assertEqual(zero.codomain.torsion_numbers, ())

    def test_normalize(self):
        A = ZModule(2, [2, 4, 8])
        B = ZModule(1, [2, 4])
        matrix = [[1, 2, 3, 4, 5],
                  [6, 7, 8, 9, 10],
                  [-1, -2, -3, -4, -5]]
        homomorphism = Homomorphism(matrix, A, B)
        self.assertEqual(homomorphism.matrix, ((1, 2, 3, 4, 5),
                                               (0, 1, 0, 1, 0),
                                               (3, 2, 1, 0, 3)))
        self.assertEqual(homomorphism.domain, A)
        self.assertEqual(homomorphism.codomain, B)

    def test_apply_zero(self):
        module = ZModule(5, [2, 2, 4, 8, 8])
        homomorphism = Homomorphism.zero(module, module)
        element = module.element([1 for _ in range(10)])
        image = homomorphism.apply(element)
        self.assertTrue(all(coordinate == 0
                            for coordinate in image.coordinates))

    def test_apply_identity(self):
        module = ZModule(5, [2, 2, 4, 8, 8])
        homomorphism = Homomorphism.zero(module, module)
        element = module.element([1 for _ in range(10)])
        image = homomorphism.apply(element)
        self.assertTrue(all(coordinate == 0
                            for coordinate in image.coordinates))

    def test_compose_with_identity(self):
        module = ZModule(2, [10])
        identity = Homomorphism.identity(module)
        matrix = (
            (1, 2, 3),
            (4, 5, 6),
            (7, 8, 9)
        )
        homomorphism = Homomorphism(matrix, domain=module, codomain=module)
        left_composition = identity.compose(homomorphism)
        self.assertEqual(left_composition.matrix, matrix)
        right_composition = homomorphism.compose(identity)
        self.assertEqual(right_composition.matrix, matrix)

    def test_homomorphism_from_canonical_generator_images(self):
        module = ZModule.free(3)
        homomorphism = Homomorphism.from_canonical_generator_images((
            module.element([1, 2, 3]),
            module.element([4, 5, 6]),
            module.element([7, 8, 9])
        ))
        self.assertEqual(homomorphism.matrix, (
            (1, 4, 7),
            (2, 5, 8),
            (3, 6, 9)
        ))
        self.assertEqual(homomorphism.domain.rank, 3)
        self.assertEqual(homomorphism.domain.torsion_numbers, ())
        self.assertEqual(homomorphism.codomain.rank, 3)
        self.assertEqual(homomorphism.codomain.torsion_numbers, ())

    def test_preimage_identity(self):
        module = ZModule.free(3)
        element = module.element([1, 2, -3])
        homomorphism = Homomorphism.identity(module)
        preimage = homomorphism.preimage(element)
        self.assertIsNotNone(preimage)
        if preimage is None:
            raise RuntimeError
        self.assertEqual(preimage.coordinates, (1, 2, -3))

    def test_preimage_zero(self):
        module = ZModule.free(3)
        element = module.element([1, 2, -3])
        homomorphism = Homomorphism.zero(module, module)
        preimage = homomorphism.preimage(element)
        self.assertIsNone(preimage)

    def test_preimage_positive(self):
        module = ZModule.free(3)
        element = module.element([1, 2, 3])
        homomorphism = Homomorphism((
            (1, 2, 3),
            (4, 5, 6),
            (7, 8, 9)
        ))

        image = homomorphism.apply(element)
        preimage = homomorphism.preimage(image)
        self.assertIsNotNone(preimage)
        if preimage is None:
            raise RuntimeError
        image_of_preimage = homomorphism.apply(preimage)
        self.assertEqual(image_of_preimage.coordinates, image.coordinates)


if __name__ == '__main__':
    unittest.main()

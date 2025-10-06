import unittest
from homology.zmodule import FinitelyGeneratedZModule
from homology.homomorphism import Homomorphism


class TestHomomorphism(unittest.TestCase):
    def test_zero(self):
        A = FinitelyGeneratedZModule(2, [])
        B = FinitelyGeneratedZModule(3, [])
        zero = Homomorphism.zero(A, B)
        self.assertEqual(
            zero.matrix,
            [[0, 0],
             [0, 0],
             [0, 0]]
        )

    def test_apply_zero(self):
        module = FinitelyGeneratedZModule(5, [2, 2, 4, 8, 8])
        homomorphism = Homomorphism.zero(module, module)
        element = module.element([1 for _ in range(10)])
        image = homomorphism.apply_to(element)
        self.assertTrue(all(coordinate == 0
                            for coordinate in image.coordinates))

    def test_apply_identity(self):
        module = FinitelyGeneratedZModule(5, [2, 2, 4, 8, 8])
        homomorphism = Homomorphism.zero(module, module)
        element = module.element([1 for _ in range(10)])
        image = homomorphism.apply_to(element)
        self.assertTrue(all(coordinate == 0
                            for coordinate in image.coordinates))


if __name__ == '__main__':
    unittest.main()

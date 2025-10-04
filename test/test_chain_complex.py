import unittest
from homology.zmodule import FinitelyGeneratedZModule
from homology.chain_complex import ChainComplex
from homology.homomorphism import Homomorphism, zero_homomorphism


class TestStringMethods(unittest.TestCase):
    def test_printing_Z(self):
        module = FinitelyGeneratedZModule(1, [])
        chain_complex = ChainComplex([module], [])
        self.assertEqual(str(chain_complex), '0 --d0--> ℤ --d1--> 0')

    def test_printing_split_sequence(self):
        A = FinitelyGeneratedZModule(1, [])
        B = FinitelyGeneratedZModule(1, [2])
        C = FinitelyGeneratedZModule(0, [2])
        chain_complex = ChainComplex(
            [A, B, C],
            [zero_homomorphism(1, 2), zero_homomorphism(2, 1)]
        )
        self.assertEqual(
            str(chain_complex),
            '0 --d0--> ℤ --d1--> ℤ ⊕ ℤ/2ℤ --d2--> ℤ/2ℤ --d3--> 0'
        )

    def test_printing_long_sequence(self):
        A = FinitelyGeneratedZModule(1, [])
        B = FinitelyGeneratedZModule(1, [2])
        C = FinitelyGeneratedZModule(0, [2])
        D = FinitelyGeneratedZModule(0, [])
        E = FinitelyGeneratedZModule(1, [])
        F = FinitelyGeneratedZModule(1, [])
        chain_complex = ChainComplex(
            [A, B, C, D, E, F],
            [zero_homomorphism(1, 2), zero_homomorphism(2, 1),
             zero_homomorphism(1, 1), zero_homomorphism(1, 1),
             Homomorphism([[1]])]
        )
        self.assertEqual(
            str(chain_complex),
            '0 --d0--> ℤ --d1--> ℤ ⊕ ℤ/2ℤ --d2--> ℤ/2ℤ --d3--> 0 --d4--> ℤ --d5--> ℤ --d6--> 0'
        )

    def test_zero_homomorphism(self):
        module = FinitelyGeneratedZModule(1, [])
        chain_complex = ChainComplex([module], [])
        self.assertEqual(chain_complex.homomorphisms[0].matrix,
                         zero_homomorphism(1, 1).matrix)


if __name__ == '__main__':
    unittest.main()

import unittest
from homology.zmodule import ZModule
from homology.homomorphism import Homomorphism
from homology.chain_complex import ChainComplex


class TestChainComplex(unittest.TestCase):
    def test_printing_Z(self):
        module = ZModule(1, [])
        chain_complex = ChainComplex([module], [])
        self.assertEqual(str(chain_complex), '0 --d0--> ℤ --d1--> 0')

    def test_printing_split_sequence(self):
        A = ZModule(1, [])
        B = ZModule(1, [2])
        C = ZModule(0, [2])
        chain_complex = ChainComplex(
            [A, B, C],
            [Homomorphism.zero(A, B), Homomorphism.zero(B, C)]
        )
        self.assertEqual(
            str(chain_complex),
            '0 --d0--> ℤ --d1--> ℤ ⊕ ℤ/2ℤ --d2--> ℤ/2ℤ --d3--> 0'
        )

    def test_printing_long_sequence(self):
        A = ZModule(1, [])
        B = ZModule(1, [2])
        C = ZModule(0, [2])
        D = ZModule(0, [])
        E = ZModule(1, [])
        F = ZModule(1, [])
        chain_complex = ChainComplex(
            [A, B, C, D, E, F],
            [Homomorphism.zero(A, B), Homomorphism.zero(B, C),
             Homomorphism.zero(C, D), Homomorphism.zero(D, E),
             Homomorphism([[1]])]
        )
        self.assertEqual(
            str(chain_complex),
            ('0 --d0--> ℤ --d1--> ℤ ⊕ ℤ/2ℤ --d2--> ℤ/2ℤ --d3--> 0 --d4--> ℤ '
             '--d5--> ℤ --d6--> 0')
        )

    def test_zero_homomorphism(self):
        module = ZModule(1, [])
        chain_complex = ChainComplex([module], [])
        self.assertEqual(chain_complex.homomorphisms[0].matrix,
                         Homomorphism.zero(module, module).matrix)


if __name__ == '__main__':
    unittest.main()

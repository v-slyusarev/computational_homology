import unittest
import textwrap
from module_theory.zmodule import ZModule
from module_theory.homomorphism import Homomorphism
from module_theory.cochain_complex import CochainComplex


class TestCochainComplex(unittest.TestCase):
    def test_printing_Z(self):
        module = ZModule(1, [])
        cochain_complex = CochainComplex([module], [])
        expected = textwrap.dedent("""\
            0 --d0--> ℤ --d1--> 0
            d1: ℤ --> 0,
            (0,)
        """)
        self.assertEqual(str(cochain_complex), expected)

    def test_printing_split_sequence(self):
        A = ZModule(1, [])
        B = ZModule(1, [2])
        C = ZModule(0, [2])
        cochain_complex = CochainComplex(
            [A, B, C],
            [Homomorphism.zero(A, B), Homomorphism.zero(B, C)]
        )
        expected = textwrap.dedent("""\
            0 --d0--> ℤ --d1--> ℤ ⊕ ℤ/2ℤ --d2--> ℤ/2ℤ --d3--> 0
            d1: ℤ --> ℤ ⊕ ℤ/2ℤ,
            (0,)
            (0,)
            d2: ℤ ⊕ ℤ/2ℤ --> ℤ/2ℤ,
            (0, 0)
            d3: ℤ/2ℤ --> 0,
            (0,)
        """)
        self.assertEqual(str(cochain_complex), expected)

    def test_printing_long_sequence(self):
        A = ZModule(1, [])
        B = ZModule(1, [2])
        C = ZModule(0, [2])
        D = ZModule(0, [])
        E = ZModule(1, [])
        F = ZModule(1, [])
        cochain_complex = CochainComplex(
            [A, B, C, D, E, F],
            [Homomorphism.zero(A, B), Homomorphism.zero(B, C),
             Homomorphism.zero(C, D), Homomorphism.zero(D, E),
             Homomorphism([[1]])]
        )
        expected = textwrap.dedent("""\
            0 --d0--> ℤ --d1--> ℤ ⊕ ℤ/2ℤ --d2--> ℤ/2ℤ --d3--> 0 --d4--> ℤ \
            --d5--> ℤ --d6--> 0
            d1: ℤ --> ℤ ⊕ ℤ/2ℤ,
            (0,)
            (0,)
            d2: ℤ ⊕ ℤ/2ℤ --> ℤ/2ℤ,
            (0, 0)
            d3: ℤ/2ℤ --> 0,
            (0,)
            d4: 0 --> ℤ,
            (0,)
            d5: ℤ --> ℤ,
            (1,)
            d6: ℤ --> 0,
            (0,)
        """)

    def test_zero_homomorphism(self):
        module = ZModule(1, [])
        cochain_complex = CochainComplex([module], [])
        self.assertEqual(cochain_complex.homomorphisms[0].matrix,
                         Homomorphism.zero(module, module).matrix)


if __name__ == '__main__':
    unittest.main()

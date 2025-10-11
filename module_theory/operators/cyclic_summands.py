from collections.abc import Sequence
from module_theory.zmodule import ZModule
from module_theory.cyclic_zmodule import FreeCyclicZModule, TorsionCyclicZModule


def cyclic_summands(module: ZModule) -> Sequence[ZModule]:
    if module.is_zero():
        return [module]

    return ([FreeCyclicZModule()] * module.rank +
            [TorsionCyclicZModule(torsion)
             for torsion in module.torsion_numbers])

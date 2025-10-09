from collections.abc import Sequence
from homology.zmodule import ZModule
from homology.cyclic_zmodule import FreeCyclicZModule, TorsionCyclicZModule


def cyclic_summands(module: ZModule) -> Sequence[ZModule]:
    if module.is_zero():
        return [module]

    return ([FreeCyclicZModule()] * module.rank +
            [TorsionCyclicZModule(torsion)
             for torsion in module.torsion_numbers])

from __future__ import annotations
from module_theory.zmodule import ZModule


class FreeCyclicZModule(ZModule):
    def __init__(self):
        super().__init__(1, [])


class TorsionCyclicZModule(ZModule):
    __match_args__: tuple[str, ...] = ("torsion",)

    def __init__(self, torsion: int):
        super().__init__(0, [torsion])
        self.torsion: int = torsion

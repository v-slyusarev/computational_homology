from __future__ import annotations
from homology.zmodule import ZModule


class FreeCyclicZModule(ZModule):
    def __init__(self):
        super().__init__(1, [])


class TorsionCyclicZModule(ZModule):
    def __init__(self, torsion: int):
        super().__init__(0, [torsion])
        self.torsion = torsion

from pycp2k.inputsection import InputSection
from ._energies2 import _energies2
from ._forces3 import _forces3
from ._forces_sigma2 import _forces_sigma2
from ._extrapolation2 import _extrapolation2
from ._sum_force1 import _sum_force1


class _print74(InputSection):
    def __init__(self):
        InputSection.__init__(self)
        self.ENERGIES = _energies2()
        self.FORCES = _forces3()
        self.FORCES_SIGMA = _forces_sigma2()
        self.EXTRAPOLATION = _extrapolation2()
        self.SUM_FORCE = _sum_force1()
        self._name = "PRINT"
        self._subsections = {'ENERGIES': 'ENERGIES', 'FORCES': 'FORCES', 'FORCES_SIGMA': 'FORCES_SIGMA', 'EXTRAPOLATION': 'EXTRAPOLATION', 'SUM_FORCE': 'SUM_FORCE'}


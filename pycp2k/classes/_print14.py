from pycp2k.inputsection import InputSection
from ._energies1 import _energies1
from ._forces_sigma1 import _forces_sigma1
from ._extrapolation1 import _extrapolation1


class _print14(InputSection):
    def __init__(self):
        InputSection.__init__(self)
        self.ENERGIES = _energies1()
        self.FORCES_SIGMA = _forces_sigma1()
        self.EXTRAPOLATION = _extrapolation1()
        self._name = "PRINT"
        self._subsections = {'ENERGIES': 'ENERGIES', 'FORCES_SIGMA': 'FORCES_SIGMA', 'EXTRAPOLATION': 'EXTRAPOLATION'}


from pycp2k.inputsection import InputSection
from ._print93 import _print93


class _block1(InputSection):
    def __init__(self):
        InputSection.__init__(self)
        self.Atoms = None
        self.Nelectron = None
        self.PRINT = _print93()
        self._name = "BLOCK"
        self._keywords = {'Atoms': 'ATOMS', 'Nelectron': 'NELECTRON'}
        self._subsections = {'PRINT': 'PRINT'}


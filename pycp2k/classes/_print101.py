from pycp2k.inputsection import InputSection
from ._vcd1 import _vcd1


class _print101(InputSection):
    def __init__(self):
        InputSection.__init__(self)
        self.VCD = _vcd1()
        self._name = "PRINT"
        self._subsections = {'VCD': 'VCD'}


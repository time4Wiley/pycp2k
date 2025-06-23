from pycp2k.inputsection import InputSection
from ._dos4 import _dos4


class _print120(InputSection):
    def __init__(self):
        InputSection.__init__(self)
        self.DOS = _dos4()
        self._name = "PRINT"
        self._subsections = {'DOS': 'DOS'}


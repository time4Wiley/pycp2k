from pycp2k.inputsection import InputSection
from ._restart15 import _restart15


class _print103(InputSection):
    def __init__(self):
        InputSection.__init__(self)
        self.RESTART = _restart15()
        self._name = "PRINT"
        self._subsections = {'RESTART': 'RESTART'}


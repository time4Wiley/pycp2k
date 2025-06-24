from pycp2k.inputsection import InputSection
from ._program_run_info61 import _program_run_info61
from ._dos5 import _dos5
from ._transmission1 import _transmission1


class _print118(InputSection):
    def __init__(self):
        InputSection.__init__(self)
        self.PROGRAM_RUN_INFO = _program_run_info61()
        self.DOS = _dos5()
        self.TRANSMISSION = _transmission1()
        self._name = "PRINT"
        self._subsections = {'PROGRAM_RUN_INFO': 'PROGRAM_RUN_INFO', 'DOS': 'DOS', 'TRANSMISSION': 'TRANSMISSION'}


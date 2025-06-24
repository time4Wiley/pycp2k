from pycp2k.inputsection import InputSection
from ._control2 import _control2
from ._parameters1 import _parameters1
from ._settings1 import _settings1
from ._mixer1 import _mixer1
from ._iterative_solver1 import _iterative_solver1
from ._print69 import _print69


class _pw_dft1(InputSection):
    def __init__(self):
        InputSection.__init__(self)
        self.CONTROL = _control2()
        self.PARAMETERS = _parameters1()
        self.SETTINGS = _settings1()
        self.MIXER = _mixer1()
        self.ITERATIVE_SOLVER = _iterative_solver1()
        self.PRINT = _print69()
        self._name = "PW_DFT"
        self._subsections = {'CONTROL': 'CONTROL', 'PARAMETERS': 'PARAMETERS', 'SETTINGS': 'SETTINGS', 'MIXER': 'MIXER', 'ITERATIVE_SOLVER': 'ITERATIVE_SOLVER', 'PRINT': 'PRINT'}


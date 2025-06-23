from pycp2k.inputsection import InputSection
from ._program_banner4 import _program_banner4
from ._guess_vectors1 import _guess_vectors1
from ._iteration_info4 import _iteration_info4
from ._detailed_energy3 import _detailed_energy3
from ._basis_set_file2 import _basis_set_file2
from ._restart14 import _restart14
from ._nto_analysis7 import _nto_analysis7
from ._mos_molden1 import _mos_molden1
from ._namd_print1 import _namd_print1
from ._soc_print1 import _soc_print1
from ._forces5 import _forces5


class _print114(InputSection):
    def __init__(self):
        InputSection.__init__(self)
        self.PROGRAM_BANNER = _program_banner4()
        self.GUESS_VECTORS = _guess_vectors1()
        self.ITERATION_INFO = _iteration_info4()
        self.DETAILED_ENERGY = _detailed_energy3()
        self.BASIS_SET_FILE = _basis_set_file2()
        self.RESTART = _restart14()
        self.NTO_ANALYSIS = _nto_analysis7()
        self.MOS_MOLDEN = _mos_molden1()
        self.NAMD_PRINT = _namd_print1()
        self.SOC_PRINT = _soc_print1()
        self.FORCES = _forces5()
        self._name = "PRINT"
        self._subsections = {'PROGRAM_BANNER': 'PROGRAM_BANNER', 'GUESS_VECTORS': 'GUESS_VECTORS', 'ITERATION_INFO': 'ITERATION_INFO', 'DETAILED_ENERGY': 'DETAILED_ENERGY', 'BASIS_SET_FILE': 'BASIS_SET_FILE', 'RESTART': 'RESTART', 'NTO_ANALYSIS': 'NTO_ANALYSIS', 'MOS_MOLDEN': 'MOS_MOLDEN', 'NAMD_PRINT': 'NAMD_PRINT', 'SOC_PRINT': 'SOC_PRINT', 'FORCES': 'FORCES'}


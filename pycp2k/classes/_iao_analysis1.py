from pycp2k.inputsection import InputSection
from ._each341 import _each341
from ._iao_molden1 import _iao_molden1
from ._iao_cubes1 import _iao_cubes1
from ._one_center_expansion1 import _one_center_expansion1
from ._bond_orbitals1 import _bond_orbitals1


class _iao_analysis1(InputSection):
    def __init__(self):
        InputSection.__init__(self)
        self.Section_parameters = None
        self.Add_last = None
        self.Common_iteration_levels = None
        self.Filename = None
        self.Log_print_key = None
        self.Eps_svd = None
        self.Eps_occ = None
        self.Atomic_charges = None
        self.EACH = _each341()
        self.IAO_MOLDEN = _iao_molden1()
        self.IAO_CUBES = _iao_cubes1()
        self.ONE_CENTER_EXPANSION = _one_center_expansion1()
        self.BOND_ORBITALS = _bond_orbitals1()
        self._name = "IAO_ANALYSIS"
        self._keywords = {'Add_last': 'ADD_LAST', 'Common_iteration_levels': 'COMMON_ITERATION_LEVELS', 'Filename': 'FILENAME', 'Log_print_key': 'LOG_PRINT_KEY', 'Eps_svd': 'EPS_SVD', 'Eps_occ': 'EPS_OCC', 'Atomic_charges': 'ATOMIC_CHARGES'}
        self._subsections = {'EACH': 'EACH', 'IAO_MOLDEN': 'IAO_MOLDEN', 'IAO_CUBES': 'IAO_CUBES', 'ONE_CENTER_EXPANSION': 'ONE_CENTER_EXPANSION', 'BOND_ORBITALS': 'BOND_ORBITALS'}
        self._attributes = ['Section_parameters']


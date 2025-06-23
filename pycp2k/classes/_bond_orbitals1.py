from pycp2k.inputsection import InputSection
from ._each345 import _each345
from ._charge_center1 import _charge_center1
from ._ibo_molden1 import _ibo_molden1
from ._ibo_cubes1 import _ibo_cubes1


class _bond_orbitals1(InputSection):
    def __init__(self):
        InputSection.__init__(self)
        self.Section_parameters = None
        self.Add_last = None
        self.Common_iteration_levels = None
        self.Filename = None
        self.Log_print_key = None
        self.Localization_operator = None
        self.Energy_localization_function = None
        self.Energy_localization_weight = None
        self.EACH = _each345()
        self.CHARGE_CENTER = _charge_center1()
        self.IBO_MOLDEN = _ibo_molden1()
        self.IBO_CUBES = _ibo_cubes1()
        self._name = "BOND_ORBITALS"
        self._keywords = {'Add_last': 'ADD_LAST', 'Common_iteration_levels': 'COMMON_ITERATION_LEVELS', 'Filename': 'FILENAME', 'Log_print_key': 'LOG_PRINT_KEY', 'Localization_operator': 'LOCALIZATION_OPERATOR', 'Energy_localization_function': 'ENERGY_LOCALIZATION_FUNCTION', 'Energy_localization_weight': 'ENERGY_LOCALIZATION_WEIGHT'}
        self._subsections = {'EACH': 'EACH', 'CHARGE_CENTER': 'CHARGE_CENTER', 'IBO_MOLDEN': 'IBO_MOLDEN', 'IBO_CUBES': 'IBO_CUBES'}
        self._attributes = ['Section_parameters']


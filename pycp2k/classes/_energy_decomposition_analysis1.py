from pycp2k.inputsection import InputSection
from ._each340 import _each340


class _energy_decomposition_analysis1(InputSection):
    def __init__(self):
        InputSection.__init__(self)
        self.Section_parameters = None
        self.Add_last = None
        self.Common_iteration_levels = None
        self.Filename = None
        self.Log_print_key = None
        self.Reference_orb_canonical = None
        self.Skip_localization = None
        self.Detailed_energy = None
        self.Ewald_alpha_parameter = None
        self.EACH = _each340()
        self._name = "ENERGY_DECOMPOSITION_ANALYSIS"
        self._keywords = {'Add_last': 'ADD_LAST', 'Common_iteration_levels': 'COMMON_ITERATION_LEVELS', 'Filename': 'FILENAME', 'Log_print_key': 'LOG_PRINT_KEY', 'Reference_orb_canonical': 'REFERENCE_ORB_CANONICAL', 'Skip_localization': 'SKIP_LOCALIZATION', 'Detailed_energy': 'DETAILED_ENERGY', 'Ewald_alpha_parameter': 'EWALD_ALPHA_PARAMETER'}
        self._subsections = {'EACH': 'EACH'}
        self._attributes = ['Section_parameters']


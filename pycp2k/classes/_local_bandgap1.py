from pycp2k.inputsection import InputSection
from ._each142 import _each142


class _local_bandgap1(InputSection):
    def __init__(self):
        InputSection.__init__(self)
        self.Section_parameters = None
        self.Add_last = None
        self.Common_iteration_levels = None
        self.Filename = None
        self.Log_print_key = None
        self.Energy_window = None
        self.Energy_spacing = None
        self.Ldos_threshold_gap = None
        self.Stride = None
        self.EACH = _each142()
        self._name = "LOCAL_BANDGAP"
        self._keywords = {'Add_last': 'ADD_LAST', 'Common_iteration_levels': 'COMMON_ITERATION_LEVELS', 'Filename': 'FILENAME', 'Log_print_key': 'LOG_PRINT_KEY', 'Energy_window': 'ENERGY_WINDOW', 'Energy_spacing': 'ENERGY_SPACING', 'Ldos_threshold_gap': 'LDOS_THRESHOLD_GAP', 'Stride': 'STRIDE'}
        self._subsections = {'EACH': 'EACH'}
        self._attributes = ['Section_parameters']


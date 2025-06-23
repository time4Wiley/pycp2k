from pycp2k.inputsection import InputSection
from ._each612 import _each612


class _nto_analysis8(InputSection):
    def __init__(self):
        InputSection.__init__(self)
        self.Section_parameters = None
        self.Add_last = None
        self.Common_iteration_levels = None
        self.Filename = None
        self.Log_print_key = None
        self.Eps_nto_eigval = None
        self.Eps_osc_str = None
        self.Num_print_exc_ntos = None
        self.State_list = None
        self.Cube_files = None
        self.Stride = None
        self.Append = None
        self.EACH = _each612()
        self._name = "NTO_ANALYSIS"
        self._keywords = {'Add_last': 'ADD_LAST', 'Common_iteration_levels': 'COMMON_ITERATION_LEVELS', 'Filename': 'FILENAME', 'Log_print_key': 'LOG_PRINT_KEY', 'Eps_nto_eigval': 'EPS_NTO_EIGVAL', 'Eps_osc_str': 'EPS_OSC_STR', 'Num_print_exc_ntos': 'NUM_PRINT_EXC_NTOS', 'State_list': 'STATE_LIST', 'Cube_files': 'CUBE_FILES', 'Stride': 'STRIDE', 'Append': 'APPEND'}
        self._subsections = {'EACH': 'EACH'}
        self._attributes = ['Section_parameters']


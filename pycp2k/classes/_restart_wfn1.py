from pycp2k.inputsection import InputSection
from ._each271 import _each271


class _restart_wfn1(InputSection):
    def __init__(self):
        InputSection.__init__(self)
        self.Section_parameters = None
        self.Add_last = None
        self.Common_iteration_levels = None
        self.Filename = None
        self.Log_print_key = None
        self.Excited_state_index = []
        self.Index = self.Excited_state_index
        self.EACH = _each271()
        self._name = "RESTART_WFN"
        self._keywords = {'Add_last': 'ADD_LAST', 'Common_iteration_levels': 'COMMON_ITERATION_LEVELS', 'Filename': 'FILENAME', 'Log_print_key': 'LOG_PRINT_KEY'}
        self._repeated_keywords = {'Excited_state_index': 'EXCITED_STATE_INDEX'}
        self._subsections = {'EACH': 'EACH'}
        self._repeated_aliases = {'Index': 'Excited_state_index'}
        self._attributes = ['Section_parameters']


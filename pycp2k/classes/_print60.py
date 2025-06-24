from pycp2k.inputsection import InputSection
from ._program_run_info25 import _program_run_info25
from ._restart11 import _restart11
from ._restart_history4 import _restart_history4
from ._field1 import _field1
from ._projection_mo1 import _projection_mo1
from ._current2 import _current2


class _print60(InputSection):
    def __init__(self):
        InputSection.__init__(self)
        self.PROGRAM_RUN_INFO = _program_run_info25()
        self.RESTART = _restart11()
        self.RESTART_HISTORY = _restart_history4()
        self.FIELD = _field1()
        self.PROJECTION_MO_list = []
        self.CURRENT = _current2()
        self._name = "PRINT"
        self._subsections = {'PROGRAM_RUN_INFO': 'PROGRAM_RUN_INFO', 'RESTART': 'RESTART', 'RESTART_HISTORY': 'RESTART_HISTORY', 'FIELD': 'FIELD', 'CURRENT': 'CURRENT'}
        self._repeated_subsections = {'PROJECTION_MO': '_projection_mo1'}
        self._attributes = ['PROJECTION_MO_list']

    def PROJECTION_MO_add(self, section_parameters=None):
        new_section = _projection_mo1()
        if section_parameters is not None:
            if hasattr(new_section, 'Section_parameters'):
                new_section.Section_parameters = section_parameters
        self.PROJECTION_MO_list.append(new_section)
        return new_section


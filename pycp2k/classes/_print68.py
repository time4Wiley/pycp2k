from pycp2k.inputsection import InputSection
from ._program_run_info25 import _program_run_info25
from ._restart11 import _restart11
from ._restart_history4 import _restart_history4
from ._field1 import _field1
from ._projection_mo1 import _projection_mo1
from ._current2 import _current2
from ._density_matrix1 import _density_matrix1
from ._moments2 import _moments2
from ._moments_ft1 import _moments_ft1
from ._polarizability1 import _polarizability1
from ._e_constituents1 import _e_constituents1


class _print68(InputSection):
    def __init__(self):
        InputSection.__init__(self)
        self.PROGRAM_RUN_INFO = _program_run_info25()
        self.RESTART = _restart11()
        self.RESTART_HISTORY = _restart_history4()
        self.FIELD = _field1()
        self.PROJECTION_MO_list = []
        self.CURRENT = _current2()
        self.DENSITY_MATRIX = _density_matrix1()
        self.MOMENTS = _moments2()
        self.MOMENTS_FT = _moments_ft1()
        self.POLARIZABILITY = _polarizability1()
        self.E_CONSTITUENTS = _e_constituents1()
        self._name = "PRINT"
        self._subsections = {'PROGRAM_RUN_INFO': 'PROGRAM_RUN_INFO', 'RESTART': 'RESTART', 'RESTART_HISTORY': 'RESTART_HISTORY', 'FIELD': 'FIELD', 'CURRENT': 'CURRENT', 'DENSITY_MATRIX': 'DENSITY_MATRIX', 'MOMENTS': 'MOMENTS', 'MOMENTS_FT': 'MOMENTS_FT', 'POLARIZABILITY': 'POLARIZABILITY', 'E_CONSTITUENTS': 'E_CONSTITUENTS'}
        self._repeated_subsections = {'PROJECTION_MO': '_projection_mo1'}
        self._attributes = ['PROJECTION_MO_list']

    def PROJECTION_MO_add(self, section_parameters=None):
        new_section = _projection_mo1()
        if section_parameters is not None:
            if hasattr(new_section, 'Section_parameters'):
                new_section.Section_parameters = section_parameters
        self.PROJECTION_MO_list.append(new_section)
        return new_section


from pycp2k.inputsection import InputSection
from ._bandstructure_path1 import _bandstructure_path1
from ._gw7 import _gw7
from ._soc2 import _soc2
from ._dos3 import _dos3


class _bandstructure1(InputSection):
    def __init__(self):
        InputSection.__init__(self)
        self.Section_parameters = None
        self.BANDSTRUCTURE_PATH_list = []
        self.GW = _gw7()
        self.SOC = _soc2()
        self.DOS = _dos3()
        self._name = "BANDSTRUCTURE"
        self._subsections = {'GW': 'GW', 'SOC': 'SOC', 'DOS': 'DOS'}
        self._repeated_subsections = {'BANDSTRUCTURE_PATH': '_bandstructure_path1'}
        self._attributes = ['Section_parameters', 'BANDSTRUCTURE_PATH_list']

    def BANDSTRUCTURE_PATH_add(self, section_parameters=None):
        new_section = _bandstructure_path1()
        if section_parameters is not None:
            if hasattr(new_section, 'Section_parameters'):
                new_section.Section_parameters = section_parameters
        self.BANDSTRUCTURE_PATH_list.append(new_section)
        return new_section


from pycp2k.inputsection import InputSection
from ._uzh20223 import _uzh20223


class _xc_kernel3(InputSection):
    def __init__(self):
        InputSection.__init__(self)
        self.Scale_x = None
        self.Scale_c = None
        self.UZH2022_list = []
        self._name = "XC_KERNEL"
        self._keywords = {'Scale_x': 'SCALE_X', 'Scale_c': 'SCALE_C'}
        self._repeated_subsections = {'UZH2022': '_uzh20223'}
        self._attributes = ['UZH2022_list']

    def UZH2022_add(self, section_parameters=None):
        new_section = _uzh20223()
        if section_parameters is not None:
            if hasattr(new_section, 'Section_parameters'):
                new_section.Section_parameters = section_parameters
        self.UZH2022_list.append(new_section)
        return new_section


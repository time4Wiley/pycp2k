from pycp2k.inputsection import InputSection
from ._hfxlr2 import _hfxlr2


class _hfx_kernel2(InputSection):
    def __init__(self):
        InputSection.__init__(self)
        self.Scale = None
        self.HFXLR_list = []
        self._name = "HFX_KERNEL"
        self._keywords = {'Scale': 'SCALE'}
        self._repeated_subsections = {'HFXLR': '_hfxlr2'}
        self._attributes = ['HFXLR_list']

    def HFXLR_add(self, section_parameters=None):
        new_section = _hfxlr2()
        if section_parameters is not None:
            if hasattr(new_section, 'Section_parameters'):
                new_section.Section_parameters = section_parameters
        self.HFXLR_list.append(new_section)
        return new_section


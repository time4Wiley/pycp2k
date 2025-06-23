from pycp2k.inputsection import InputSection
from ._hf6 import _hf6
from ._hfxlr2 import _hfxlr2


class _hfx_kernel2(InputSection):
    def __init__(self):
        InputSection.__init__(self)
        self.Do_hfxsr = None
        self.Hfxsr_primbas = None
        self.HF_list = []
        self.HFXLR = _hfxlr2()
        self._name = "HFX_KERNEL"
        self._keywords = {'Do_hfxsr': 'DO_HFXSR', 'Hfxsr_primbas': 'HFXSR_PRIMBAS'}
        self._subsections = {'HFXLR': 'HFXLR'}
        self._repeated_subsections = {'HF': '_hf6'}
        self._attributes = ['HF_list']

    def HF_add(self, section_parameters=None):
        new_section = _hf6()
        if section_parameters is not None:
            if hasattr(new_section, 'Section_parameters'):
                new_section.Section_parameters = section_parameters
        self.HF_list.append(new_section)
        return new_section


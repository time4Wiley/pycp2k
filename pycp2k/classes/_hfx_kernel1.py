from pycp2k.inputsection import InputSection
from ._hf3 import _hf3
from ._hfxlr1 import _hfxlr1


class _hfx_kernel1(InputSection):
    def __init__(self):
        InputSection.__init__(self)
        self.Do_hfxsr = None
        self.Hfxsr_primbas = None
        self.HF_list = []
        self.HFXLR = _hfxlr1()
        self._name = "HFX_KERNEL"
        self._keywords = {'Do_hfxsr': 'DO_HFXSR', 'Hfxsr_primbas': 'HFXSR_PRIMBAS'}
        self._subsections = {'HFXLR': 'HFXLR'}
        self._repeated_subsections = {'HF': '_hf3'}
        self._attributes = ['HF_list']

    def HF_add(self, section_parameters=None):
        new_section = _hf3()
        if section_parameters is not None:
            if hasattr(new_section, 'Section_parameters'):
                new_section.Section_parameters = section_parameters
        self.HF_list.append(new_section)
        return new_section


from pycp2k.inputsection import InputSection
from ._hf_info16 import _hf_info16
from ._periodic17 import _periodic17
from ._screening17 import _screening17
from ._interaction_potential21 import _interaction_potential21
from ._load_balance16 import _load_balance16
from ._memory17 import _memory17
from ._ri21 import _ri21


class _hf16(InputSection):
    def __init__(self):
        InputSection.__init__(self)
        self.Fraction = None
        self.Treat_lsd_in_core = None
        self.Pw_hfx = None
        self.Pw_hfx_blocksize = None
        self.HF_INFO = _hf_info16()
        self.PERIODIC = _periodic17()
        self.SCREENING = _screening17()
        self.INTERACTION_POTENTIAL = _interaction_potential21()
        self.LOAD_BALANCE = _load_balance16()
        self.MEMORY = _memory17()
        self.RI = _ri21()
        self._name = "HF"
        self._keywords = {'Fraction': 'FRACTION', 'Treat_lsd_in_core': 'TREAT_LSD_IN_CORE', 'Pw_hfx': 'PW_HFX', 'Pw_hfx_blocksize': 'PW_HFX_BLOCKSIZE'}
        self._subsections = {'HF_INFO': 'HF_INFO', 'PERIODIC': 'PERIODIC', 'SCREENING': 'SCREENING', 'INTERACTION_POTENTIAL': 'INTERACTION_POTENTIAL', 'LOAD_BALANCE': 'LOAD_BALANCE', 'MEMORY': 'MEMORY', 'RI': 'RI'}


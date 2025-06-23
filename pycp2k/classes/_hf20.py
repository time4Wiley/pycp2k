from pycp2k.inputsection import InputSection
from ._hf_info20 import _hf_info20
from ._periodic21 import _periodic21
from ._screening21 import _screening21
from ._interaction_potential26 import _interaction_potential26
from ._load_balance20 import _load_balance20
from ._memory21 import _memory21
from ._ri26 import _ri26


class _hf20(InputSection):
    def __init__(self):
        InputSection.__init__(self)
        self.Fraction = None
        self.Treat_lsd_in_core = None
        self.Pw_hfx = None
        self.Pw_hfx_blocksize = None
        self.HF_INFO = _hf_info20()
        self.PERIODIC = _periodic21()
        self.SCREENING = _screening21()
        self.INTERACTION_POTENTIAL = _interaction_potential26()
        self.LOAD_BALANCE = _load_balance20()
        self.MEMORY = _memory21()
        self.RI = _ri26()
        self._name = "HF"
        self._keywords = {'Fraction': 'FRACTION', 'Treat_lsd_in_core': 'TREAT_LSD_IN_CORE', 'Pw_hfx': 'PW_HFX', 'Pw_hfx_blocksize': 'PW_HFX_BLOCKSIZE'}
        self._subsections = {'HF_INFO': 'HF_INFO', 'PERIODIC': 'PERIODIC', 'SCREENING': 'SCREENING', 'INTERACTION_POTENTIAL': 'INTERACTION_POTENTIAL', 'LOAD_BALANCE': 'LOAD_BALANCE', 'MEMORY': 'MEMORY', 'RI': 'RI'}


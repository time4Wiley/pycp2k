from pycp2k.inputsection import InputSection
from ._hf_info17 import _hf_info17
from ._periodic18 import _periodic18
from ._screening18 import _screening18
from ._interaction_potential22 import _interaction_potential22
from ._load_balance17 import _load_balance17
from ._memory18 import _memory18
from ._ri22 import _ri22


class _hf17(InputSection):
    def __init__(self):
        InputSection.__init__(self)
        self.Fraction = None
        self.Treat_lsd_in_core = None
        self.Pw_hfx = None
        self.Pw_hfx_blocksize = None
        self.HF_INFO = _hf_info17()
        self.PERIODIC = _periodic18()
        self.SCREENING = _screening18()
        self.INTERACTION_POTENTIAL = _interaction_potential22()
        self.LOAD_BALANCE = _load_balance17()
        self.MEMORY = _memory18()
        self.RI = _ri22()
        self._name = "HF"
        self._keywords = {'Fraction': 'FRACTION', 'Treat_lsd_in_core': 'TREAT_LSD_IN_CORE', 'Pw_hfx': 'PW_HFX', 'Pw_hfx_blocksize': 'PW_HFX_BLOCKSIZE'}
        self._subsections = {'HF_INFO': 'HF_INFO', 'PERIODIC': 'PERIODIC', 'SCREENING': 'SCREENING', 'INTERACTION_POTENTIAL': 'INTERACTION_POTENTIAL', 'LOAD_BALANCE': 'LOAD_BALANCE', 'MEMORY': 'MEMORY', 'RI': 'RI'}


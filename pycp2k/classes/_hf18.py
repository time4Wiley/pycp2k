from pycp2k.inputsection import InputSection
from ._hf_info18 import _hf_info18
from ._periodic19 import _periodic19
from ._screening19 import _screening19
from ._interaction_potential24 import _interaction_potential24
from ._load_balance18 import _load_balance18
from ._memory19 import _memory19
from ._ri24 import _ri24


class _hf18(InputSection):
    def __init__(self):
        InputSection.__init__(self)
        self.Fraction = None
        self.Treat_lsd_in_core = None
        self.Pw_hfx = None
        self.Pw_hfx_blocksize = None
        self.HF_INFO = _hf_info18()
        self.PERIODIC = _periodic19()
        self.SCREENING = _screening19()
        self.INTERACTION_POTENTIAL = _interaction_potential24()
        self.LOAD_BALANCE = _load_balance18()
        self.MEMORY = _memory19()
        self.RI = _ri24()
        self._name = "HF"
        self._keywords = {'Fraction': 'FRACTION', 'Treat_lsd_in_core': 'TREAT_LSD_IN_CORE', 'Pw_hfx': 'PW_HFX', 'Pw_hfx_blocksize': 'PW_HFX_BLOCKSIZE'}
        self._subsections = {'HF_INFO': 'HF_INFO', 'PERIODIC': 'PERIODIC', 'SCREENING': 'SCREENING', 'INTERACTION_POTENTIAL': 'INTERACTION_POTENTIAL', 'LOAD_BALANCE': 'LOAD_BALANCE', 'MEMORY': 'MEMORY', 'RI': 'RI'}


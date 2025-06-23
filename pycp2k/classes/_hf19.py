from pycp2k.inputsection import InputSection
from ._hf_info19 import _hf_info19
from ._periodic20 import _periodic20
from ._screening20 import _screening20
from ._interaction_potential25 import _interaction_potential25
from ._load_balance19 import _load_balance19
from ._memory20 import _memory20
from ._ri25 import _ri25


class _hf19(InputSection):
    def __init__(self):
        InputSection.__init__(self)
        self.Fraction = None
        self.Treat_lsd_in_core = None
        self.Pw_hfx = None
        self.Pw_hfx_blocksize = None
        self.HF_INFO = _hf_info19()
        self.PERIODIC = _periodic20()
        self.SCREENING = _screening20()
        self.INTERACTION_POTENTIAL = _interaction_potential25()
        self.LOAD_BALANCE = _load_balance19()
        self.MEMORY = _memory20()
        self.RI = _ri25()
        self._name = "HF"
        self._keywords = {'Fraction': 'FRACTION', 'Treat_lsd_in_core': 'TREAT_LSD_IN_CORE', 'Pw_hfx': 'PW_HFX', 'Pw_hfx_blocksize': 'PW_HFX_BLOCKSIZE'}
        self._subsections = {'HF_INFO': 'HF_INFO', 'PERIODIC': 'PERIODIC', 'SCREENING': 'SCREENING', 'INTERACTION_POTENTIAL': 'INTERACTION_POTENTIAL', 'LOAD_BALANCE': 'LOAD_BALANCE', 'MEMORY': 'MEMORY', 'RI': 'RI'}


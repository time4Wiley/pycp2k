from pycp2k.inputsection import InputSection
from ._hf_info9 import _hf_info9
from ._periodic9 import _periodic9
from ._screening10 import _screening10
from ._interaction_potential12 import _interaction_potential12
from ._load_balance9 import _load_balance9
from ._memory10 import _memory10
from ._ri12 import _ri12


class _hf9(InputSection):
    def __init__(self):
        InputSection.__init__(self)
        self.Fraction = None
        self.Treat_lsd_in_core = None
        self.Pw_hfx = None
        self.Pw_hfx_blocksize = None
        self.HF_INFO = _hf_info9()
        self.PERIODIC = _periodic9()
        self.SCREENING = _screening10()
        self.INTERACTION_POTENTIAL = _interaction_potential12()
        self.LOAD_BALANCE = _load_balance9()
        self.MEMORY = _memory10()
        self.RI = _ri12()
        self._name = "HF"
        self._keywords = {'Fraction': 'FRACTION', 'Treat_lsd_in_core': 'TREAT_LSD_IN_CORE', 'Pw_hfx': 'PW_HFX', 'Pw_hfx_blocksize': 'PW_HFX_BLOCKSIZE'}
        self._subsections = {'HF_INFO': 'HF_INFO', 'PERIODIC': 'PERIODIC', 'SCREENING': 'SCREENING', 'INTERACTION_POTENTIAL': 'INTERACTION_POTENTIAL', 'LOAD_BALANCE': 'LOAD_BALANCE', 'MEMORY': 'MEMORY', 'RI': 'RI'}


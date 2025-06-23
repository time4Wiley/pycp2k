from pycp2k.inputsection import InputSection
from ._hf_info21 import _hf_info21
from ._periodic22 import _periodic22
from ._screening22 import _screening22
from ._interaction_potential28 import _interaction_potential28
from ._load_balance21 import _load_balance21
from ._memory22 import _memory22
from ._ri28 import _ri28


class _hf21(InputSection):
    def __init__(self):
        InputSection.__init__(self)
        self.Fraction = None
        self.Treat_lsd_in_core = None
        self.Pw_hfx = None
        self.Pw_hfx_blocksize = None
        self.HF_INFO = _hf_info21()
        self.PERIODIC = _periodic22()
        self.SCREENING = _screening22()
        self.INTERACTION_POTENTIAL = _interaction_potential28()
        self.LOAD_BALANCE = _load_balance21()
        self.MEMORY = _memory22()
        self.RI = _ri28()
        self._name = "HF"
        self._keywords = {'Fraction': 'FRACTION', 'Treat_lsd_in_core': 'TREAT_LSD_IN_CORE', 'Pw_hfx': 'PW_HFX', 'Pw_hfx_blocksize': 'PW_HFX_BLOCKSIZE'}
        self._subsections = {'HF_INFO': 'HF_INFO', 'PERIODIC': 'PERIODIC', 'SCREENING': 'SCREENING', 'INTERACTION_POTENTIAL': 'INTERACTION_POTENTIAL', 'LOAD_BALANCE': 'LOAD_BALANCE', 'MEMORY': 'MEMORY', 'RI': 'RI'}


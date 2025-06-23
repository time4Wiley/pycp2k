from pycp2k.inputsection import InputSection
from ._hf_info15 import _hf_info15
from ._periodic16 import _periodic16
from ._screening16 import _screening16
from ._interaction_potential20 import _interaction_potential20
from ._load_balance15 import _load_balance15
from ._memory16 import _memory16
from ._ri20 import _ri20


class _hf15(InputSection):
    def __init__(self):
        InputSection.__init__(self)
        self.Fraction = None
        self.Treat_lsd_in_core = None
        self.Pw_hfx = None
        self.Pw_hfx_blocksize = None
        self.HF_INFO = _hf_info15()
        self.PERIODIC = _periodic16()
        self.SCREENING = _screening16()
        self.INTERACTION_POTENTIAL = _interaction_potential20()
        self.LOAD_BALANCE = _load_balance15()
        self.MEMORY = _memory16()
        self.RI = _ri20()
        self._name = "HF"
        self._keywords = {'Fraction': 'FRACTION', 'Treat_lsd_in_core': 'TREAT_LSD_IN_CORE', 'Pw_hfx': 'PW_HFX', 'Pw_hfx_blocksize': 'PW_HFX_BLOCKSIZE'}
        self._subsections = {'HF_INFO': 'HF_INFO', 'PERIODIC': 'PERIODIC', 'SCREENING': 'SCREENING', 'INTERACTION_POTENTIAL': 'INTERACTION_POTENTIAL', 'LOAD_BALANCE': 'LOAD_BALANCE', 'MEMORY': 'MEMORY', 'RI': 'RI'}


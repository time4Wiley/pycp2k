from pycp2k.inputsection import InputSection
from ._local_bandgap5 import _local_bandgap5
from ._gw_dos5 import _gw_dos5


class _print86(InputSection):
    def __init__(self):
        InputSection.__init__(self)
        self.LOCAL_BANDGAP = _local_bandgap5()
        self.GW_DOS = _gw_dos5()
        self._name = "PRINT"
        self._subsections = {'LOCAL_BANDGAP': 'LOCAL_BANDGAP', 'GW_DOS': 'GW_DOS'}


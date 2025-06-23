from pycp2k.inputsection import InputSection
from ._local_bandgap2 import _local_bandgap2
from ._gw_dos2 import _gw_dos2


class _print38(InputSection):
    def __init__(self):
        InputSection.__init__(self)
        self.LOCAL_BANDGAP = _local_bandgap2()
        self.GW_DOS = _gw_dos2()
        self._name = "PRINT"
        self._subsections = {'LOCAL_BANDGAP': 'LOCAL_BANDGAP', 'GW_DOS': 'GW_DOS'}


from pycp2k.inputsection import InputSection
from ._local_bandgap1 import _local_bandgap1
from ._gw_dos1 import _gw_dos1


class _print29(InputSection):
    def __init__(self):
        InputSection.__init__(self)
        self.LOCAL_BANDGAP = _local_bandgap1()
        self.GW_DOS = _gw_dos1()
        self._name = "PRINT"
        self._subsections = {'LOCAL_BANDGAP': 'LOCAL_BANDGAP', 'GW_DOS': 'GW_DOS'}


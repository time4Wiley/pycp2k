from pycp2k.inputsection import InputSection
from ._local_bandgap3 import _local_bandgap3
from ._gw_dos3 import _gw_dos3


class _print48(InputSection):
    def __init__(self):
        InputSection.__init__(self)
        self.LOCAL_BANDGAP = _local_bandgap3()
        self.GW_DOS = _gw_dos3()
        self._name = "PRINT"
        self._subsections = {'LOCAL_BANDGAP': 'LOCAL_BANDGAP', 'GW_DOS': 'GW_DOS'}


from pycp2k.inputsection import InputSection
from ._local_bandgap6 import _local_bandgap6
from ._gw_dos6 import _gw_dos6


class _print100(InputSection):
    def __init__(self):
        InputSection.__init__(self)
        self.LOCAL_BANDGAP = _local_bandgap6()
        self.GW_DOS = _gw_dos6()
        self._name = "PRINT"
        self._subsections = {'LOCAL_BANDGAP': 'LOCAL_BANDGAP', 'GW_DOS': 'GW_DOS'}


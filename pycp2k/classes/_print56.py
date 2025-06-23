from pycp2k.inputsection import InputSection
from ._local_bandgap4 import _local_bandgap4
from ._gw_dos4 import _gw_dos4


class _print56(InputSection):
    def __init__(self):
        InputSection.__init__(self)
        self.LOCAL_BANDGAP = _local_bandgap4()
        self.GW_DOS = _gw_dos4()
        self._name = "PRINT"
        self._subsections = {'LOCAL_BANDGAP': 'LOCAL_BANDGAP', 'GW_DOS': 'GW_DOS'}


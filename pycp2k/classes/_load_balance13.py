from pycp2k.inputsection import InputSection
from ._print120 import _print120


class _load_balance13(InputSection):
    def __init__(self):
        InputSection.__init__(self)
        self.Nbins = None
        self.Block_size = None
        self.Randomize = None
        self.PRINT = _print120()
        self._name = "LOAD_BALANCE"
        self._keywords = {'Nbins': 'NBINS', 'Block_size': 'BLOCK_SIZE', 'Randomize': 'RANDOMIZE'}
        self._subsections = {'PRINT': 'PRINT'}


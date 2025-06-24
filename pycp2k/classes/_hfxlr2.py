from pycp2k.inputsection import InputSection


class _hfxlr2(InputSection):
    def __init__(self):
        InputSection.__init__(self)
        self.Alpha = None
        self.Beta = None
        self._name = "HFXLR"
        self._keywords = {'Alpha': 'ALPHA', 'Beta': 'BETA'}


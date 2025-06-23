from pycp2k.inputsection import InputSection


class _hfxlr6(InputSection):
    def __init__(self):
        InputSection.__init__(self)
        self.Rcut = None
        self.Scale = None
        self._name = "HFXLR"
        self._keywords = {'Rcut': 'RCUT', 'Scale': 'SCALE'}


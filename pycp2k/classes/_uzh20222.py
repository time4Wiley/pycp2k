from pycp2k.inputsection import InputSection


class _uzh20222(InputSection):
    def __init__(self):
        InputSection.__init__(self)
        self.Alpha = None
        self.Beta = None
        self._name = "UZH2022"
        self._keywords = {'Alpha': 'ALPHA', 'Beta': 'BETA'}


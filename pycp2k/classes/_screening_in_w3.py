from pycp2k.inputsection import InputSection


class _screening_in_w3(InputSection):
    def __init__(self):
        InputSection.__init__(self)
        self.Section_parameters = None
        self.Alpha = None
        self._name = "SCREENING_IN_W"
        self._keywords = {'Alpha': 'ALPHA'}
        self._attributes = ['Section_parameters']


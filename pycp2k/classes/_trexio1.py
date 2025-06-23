from pycp2k.inputsection import InputSection


class _trexio1(InputSection):
    def __init__(self):
        InputSection.__init__(self)
        self.Filename = None
        self.Cartesian = None
        self._name = "TREXIO"
        self._keywords = {'Filename': 'FILENAME', 'Cartesian': 'CARTESIAN'}


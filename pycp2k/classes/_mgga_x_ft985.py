from pycp2k.inputsection import InputSection


class _mgga_x_ft985(InputSection):
    def __init__(self):
        InputSection.__init__(self)
        self.Section_parameters = None
        self.Scale = None
        self._a = None
        self._b = None
        self._a1 = None
        self._a2 = None
        self._b1 = None
        self._b2 = None
        self._name = "MGGA_X_FT98"
        self._keywords = {'Scale': 'SCALE', '_a': '_A', '_b': '_B', '_a1': '_A1', '_a2': '_A2', '_b1': '_B1', '_b2': '_B2'}
        self._attributes = ['Section_parameters']


from pycp2k.inputsection import InputSection


class _mgga_x_eel4(InputSection):
    def __init__(self):
        InputSection.__init__(self)
        self.Section_parameters = None
        self.Scale = None
        self._c = None
        self._x0 = None
        self._a0 = None
        self._name = "MGGA_X_EEL"
        self._keywords = {'Scale': 'SCALE', '_c': '_C', '_x0': '_X0', '_a0': '_A0'}
        self._attributes = ['Section_parameters']


from pycp2k.inputsection import InputSection


class _gga_x_hcth_a5(InputSection):
    def __init__(self):
        InputSection.__init__(self)
        self.Section_parameters = None
        self.Scale = None
        self._beta = None
        self._gamma = None
        self._c0 = None
        self._c1 = None
        self._c2 = None
        self._name = "GGA_X_HCTH_A"
        self._keywords = {'Scale': 'SCALE', '_beta': '_BETA', '_gamma': '_GAMMA', '_c0': '_C0', '_c1': '_C1', '_c2': '_C2'}
        self._attributes = ['Section_parameters']


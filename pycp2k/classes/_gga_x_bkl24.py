from pycp2k.inputsection import InputSection


class _gga_x_bkl24(InputSection):
    def __init__(self):
        InputSection.__init__(self)
        self.Section_parameters = None
        self.Scale = None
        self._mu1 = None
        self._kappa = None
        self._alpha = None
        self._beta = None
        self._gamma = None
        self._name = "GGA_X_BKL2"
        self._keywords = {'Scale': 'SCALE', '_mu1': '_MU1', '_kappa': '_KAPPA', '_alpha': '_ALPHA', '_beta': '_BETA', '_gamma': '_GAMMA'}
        self._attributes = ['Section_parameters']


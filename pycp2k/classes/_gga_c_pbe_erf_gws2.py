from pycp2k.inputsection import InputSection


class _gga_c_pbe_erf_gws2(InputSection):
    def __init__(self):
        InputSection.__init__(self)
        self.Section_parameters = None
        self.Scale = None
        self._beta = None
        self._gamma = None
        self._a_c = None
        self._omega = None
        self._name = "GGA_C_PBE_ERF_GWS"
        self._keywords = {'Scale': 'SCALE', '_beta': '_BETA', '_gamma': '_GAMMA', '_a_c': '_A_C', '_omega': '_OMEGA'}
        self._attributes = ['Section_parameters']


from pycp2k.inputsection import InputSection


class _hyb_gga_xc_lc_vv105(InputSection):
    def __init__(self):
        InputSection.__init__(self)
        self.Section_parameters = None
        self.Scale = None
        self._b = None
        self._c = None
        self._alpha = None
        self._beta = None
        self._omega = None
        self._name = "HYB_GGA_XC_LC_VV10"
        self._keywords = {'Scale': 'SCALE', '_b': '_B', '_c': '_C', '_alpha': '_ALPHA', '_beta': '_BETA', '_omega': '_OMEGA'}
        self._attributes = ['Section_parameters']


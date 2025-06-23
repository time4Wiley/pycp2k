from pycp2k.inputsection import InputSection


class _hyb_gga_xc_camy_b3lyp5(InputSection):
    def __init__(self):
        InputSection.__init__(self)
        self.Section_parameters = None
        self.Scale = None
        self._ac = None
        self._alpha = None
        self._beta = None
        self._omega = None
        self._name = "HYB_GGA_XC_CAMY_B3LYP"
        self._keywords = {'Scale': 'SCALE', '_ac': '_AC', '_alpha': '_ALPHA', '_beta': '_BETA', '_omega': '_OMEGA'}
        self._attributes = ['Section_parameters']


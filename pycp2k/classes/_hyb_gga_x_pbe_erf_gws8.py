from pycp2k.inputsection import InputSection


class _hyb_gga_x_pbe_erf_gws8(InputSection):
    def __init__(self):
        InputSection.__init__(self)
        self.Section_parameters = None
        self.Scale = None
        self._kappa = None
        self._b_pbe = None
        self._ax = None
        self._omega = None
        self._name = "HYB_GGA_X_PBE_ERF_GWS"
        self._keywords = {'Scale': 'SCALE', '_kappa': '_KAPPA', '_b_pbe': '_B_PBE', '_ax': '_AX', '_omega': '_OMEGA'}
        self._attributes = ['Section_parameters']


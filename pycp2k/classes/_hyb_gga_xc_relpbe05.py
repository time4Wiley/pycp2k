from pycp2k.inputsection import InputSection


class _hyb_gga_xc_relpbe05(InputSection):
    def __init__(self):
        InputSection.__init__(self)
        self.Section_parameters = None
        self.Scale = None
        self._cx = None
        self._scalggac = None
        self._scalldac = None
        self._xkappa = None
        self._cbetapbe = None
        self._xmuepbe = None
        self._name = "HYB_GGA_XC_RELPBE0"
        self._keywords = {'Scale': 'SCALE', '_cx': '_CX', '_scalggac': '_SCALGGAC', '_scalldac': '_SCALLDAC', '_xkappa': '_XKAPPA', '_cbetapbe': '_CBETAPBE', '_xmuepbe': '_XMUEPBE'}
        self._attributes = ['Section_parameters']


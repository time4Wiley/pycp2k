from pycp2k.inputsection import InputSection


class _hyb_mgga_xc_br3p868(InputSection):
    def __init__(self):
        InputSection.__init__(self)
        self.Section_parameters = None
        self.Scale = None
        self._a = None
        self._b = None
        self._c = None
        self._name = "HYB_MGGA_XC_BR3P86"
        self._keywords = {'Scale': 'SCALE', '_a': '_A', '_b': '_B', '_c': '_C'}
        self._attributes = ['Section_parameters']


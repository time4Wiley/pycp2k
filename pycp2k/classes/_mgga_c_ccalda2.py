from pycp2k.inputsection import InputSection


class _mgga_c_ccalda2(InputSection):
    def __init__(self):
        InputSection.__init__(self)
        self.Section_parameters = None
        self.Scale = None
        self._c = None
        self._name = "MGGA_C_CCALDA"
        self._keywords = {'Scale': 'SCALE', '_c': '_C'}
        self._attributes = ['Section_parameters']


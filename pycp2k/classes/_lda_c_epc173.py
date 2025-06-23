from pycp2k.inputsection import InputSection


class _lda_c_epc173(InputSection):
    def __init__(self):
        InputSection.__init__(self)
        self.Section_parameters = None
        self.Scale = None
        self._a = None
        self._b = None
        self._c = None
        self._name = "LDA_C_EPC17"
        self._keywords = {'Scale': 'SCALE', '_a': '_A', '_b': '_B', '_c': '_C'}
        self._attributes = ['Section_parameters']


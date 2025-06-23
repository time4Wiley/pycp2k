from pycp2k.inputsection import InputSection


class _lda_c_pw_erf2(InputSection):
    def __init__(self):
        InputSection.__init__(self)
        self.Section_parameters = None
        self.Scale = None
        self.Short_range_omega = None
        self._name = "LDA_C_PW_ERF"
        self._keywords = {'Scale': 'SCALE', 'Short_range_omega': 'SHORT_RANGE_OMEGA'}
        self._attributes = ['Section_parameters']


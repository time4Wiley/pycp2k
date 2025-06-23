from pycp2k.inputsection import InputSection


class _mgga_x_ktbm_36(InputSection):
    def __init__(self):
        InputSection.__init__(self)
        self.Section_parameters = None
        self.Scale = None
        self.Ct = None
        self.At = None
        self.Bt = None
        self.A2t = None
        self.B2t = None
        self.Xt = None
        self.Cb = None
        self.Ab = None
        self.Bb = None
        self.A2b = None
        self.B2b = None
        self.Xb = None
        self._name = "MGGA_X_KTBM_3"
        self._keywords = {'Scale': 'SCALE', 'Ct': 'CT', 'At': 'AT', 'Bt': 'BT', 'A2t': 'A2T', 'B2t': 'B2T', 'Xt': 'XT', 'Cb': 'CB', 'Ab': 'AB', 'Bb': 'BB', 'A2b': 'A2B', 'B2b': 'B2B', 'Xb': 'XB'}
        self._attributes = ['Section_parameters']


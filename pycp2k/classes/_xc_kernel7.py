from pycp2k.inputsection import InputSection


class _xc_kernel7(InputSection):
    def __init__(self):
        InputSection.__init__(self)
        self.Section_parameters = None
        self.Parameter = None
        self.Gamma = None
        self.C_xaa = None
        self.C_cab = None
        self.C_caa = None
        self.Scale_x = None
        self.Scale_c = None
        self._name = "XC_KERNEL"
        self._keywords = {'Parameter': 'PARAMETER', 'Gamma': 'GAMMA', 'C_xaa': 'C_XAA', 'C_cab': 'C_CAB', 'C_caa': 'C_CAA', 'Scale_x': 'SCALE_X', 'Scale_c': 'SCALE_C'}
        self._attributes = ['Section_parameters']


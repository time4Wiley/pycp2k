from pycp2k.inputsection import InputSection


class _hyb_mgga_xc_gas221(InputSection):
    def __init__(self):
        InputSection.__init__(self)
        self.Section_parameters = None
        self.Scale = None
        self._cx00 = None
        self._cx01 = None
        self._cx10 = None
        self._css00 = None
        self._css04 = None
        self._css10 = None
        self._css20 = None
        self._css43 = None
        self._cos00 = None
        self._cos10 = None
        self._cos20 = None
        self._cos21 = None
        self._cos60 = None
        self._alpha = None
        self._beta = None
        self._omega = None
        self._name = "HYB_MGGA_XC_GAS22"
        self._keywords = {'Scale': 'SCALE', '_cx00': '_CX00', '_cx01': '_CX01', '_cx10': '_CX10', '_css00': '_CSS00', '_css04': '_CSS04', '_css10': '_CSS10', '_css20': '_CSS20', '_css43': '_CSS43', '_cos00': '_COS00', '_cos10': '_COS10', '_cos20': '_COS20', '_cos21': '_COS21', '_cos60': '_COS60', '_alpha': '_ALPHA', '_beta': '_BETA', '_omega': '_OMEGA'}
        self._attributes = ['Section_parameters']


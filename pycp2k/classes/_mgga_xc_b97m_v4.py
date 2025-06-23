from pycp2k.inputsection import InputSection


class _mgga_xc_b97m_v4(InputSection):
    def __init__(self):
        InputSection.__init__(self)
        self.Section_parameters = None
        self.Scale = None
        self._cx00 = None
        self._cx01 = None
        self._cx02 = None
        self._cx10 = None
        self._cx11 = None
        self._css00 = None
        self._css02 = None
        self._css10 = None
        self._css32 = None
        self._css42 = None
        self._cos00 = None
        self._cos01 = None
        self._cos03 = None
        self._cos10 = None
        self._cos32 = None
        self._name = "MGGA_XC_B97M_V"
        self._keywords = {'Scale': 'SCALE', '_cx00': '_CX00', '_cx01': '_CX01', '_cx02': '_CX02', '_cx10': '_CX10', '_cx11': '_CX11', '_css00': '_CSS00', '_css02': '_CSS02', '_css10': '_CSS10', '_css32': '_CSS32', '_css42': '_CSS42', '_cos00': '_COS00', '_cos01': '_COS01', '_cos03': '_COS03', '_cos10': '_COS10', '_cos32': '_COS32'}
        self._attributes = ['Section_parameters']


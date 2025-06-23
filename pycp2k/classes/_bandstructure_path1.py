from pycp2k.inputsection import InputSection


class _bandstructure_path1(InputSection):
    def __init__(self):
        InputSection.__init__(self)
        self.Special_point = []
        self.Npoints = None
        self.Units = None
        self._name = "BANDSTRUCTURE_PATH"
        self._keywords = {'Npoints': 'NPOINTS', 'Units': 'UNITS'}
        self._repeated_keywords = {'Special_point': 'SPECIAL_POINT'}


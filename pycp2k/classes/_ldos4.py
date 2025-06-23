from pycp2k.inputsection import InputSection


class _ldos4(InputSection):
    def __init__(self):
        InputSection.__init__(self)
        self.Section_parameters = None
        self.Integration = None
        self.Bin_mesh = None
        self._name = "LDOS"
        self._keywords = {'Integration': 'INTEGRATION', 'Bin_mesh': 'BIN_MESH'}
        self._attributes = ['Section_parameters']


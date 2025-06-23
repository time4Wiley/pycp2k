from pycp2k.inputsection import InputSection


class _soc2(InputSection):
    def __init__(self):
        InputSection.__init__(self)
        self.Section_parameters = None
        self.Energy_window = None
        self._name = "SOC"
        self._keywords = {'Energy_window': 'ENERGY_WINDOW'}
        self._attributes = ['Section_parameters']


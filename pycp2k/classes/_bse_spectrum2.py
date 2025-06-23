from pycp2k.inputsection import InputSection


class _bse_spectrum2(InputSection):
    def __init__(self):
        InputSection.__init__(self)
        self.Section_parameters = None
        self.Frequency_step_size = None
        self.Frequency_starting_point = None
        self.Frequency_end_point = None
        self.Eta_list = None
        self._name = "BSE_SPECTRUM"
        self._keywords = {'Frequency_step_size': 'FREQUENCY_STEP_SIZE', 'Frequency_starting_point': 'FREQUENCY_STARTING_POINT', 'Frequency_end_point': 'FREQUENCY_END_POINT', 'Eta_list': 'ETA_LIST'}
        self._attributes = ['Section_parameters']


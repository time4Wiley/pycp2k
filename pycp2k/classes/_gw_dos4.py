from pycp2k.inputsection import InputSection


class _gw_dos4(InputSection):
    def __init__(self):
        InputSection.__init__(self)
        self.Lower_bound = None
        self.Upper_bound = None
        self.Step = None
        self.Min_level_spectral = None
        self.Max_level_spectral = None
        self.Min_level_self_energy = None
        self.Max_level_self_energy = None
        self.Broadening = None
        self._name = "GW_DOS"
        self._keywords = {'Lower_bound': 'LOWER_BOUND', 'Upper_bound': 'UPPER_BOUND', 'Step': 'STEP', 'Min_level_spectral': 'MIN_LEVEL_SPECTRAL', 'Max_level_spectral': 'MAX_LEVEL_SPECTRAL', 'Min_level_self_energy': 'MIN_LEVEL_SELF_ENERGY', 'Max_level_self_energy': 'MAX_LEVEL_SELF_ENERGY', 'Broadening': 'BROADENING'}


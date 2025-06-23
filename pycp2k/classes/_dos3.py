from pycp2k.inputsection import InputSection
from ._ldos4 import _ldos4


class _dos3(InputSection):
    def __init__(self):
        InputSection.__init__(self)
        self.Section_parameters = None
        self.Energy_window = None
        self.Energy_step = None
        self.Broadening = None
        self.Kpoints = None
        self.LDOS = _ldos4()
        self._name = "DOS"
        self._keywords = {'Energy_window': 'ENERGY_WINDOW', 'Energy_step': 'ENERGY_STEP', 'Broadening': 'BROADENING', 'Kpoints': 'KPOINTS'}
        self._subsections = {'LDOS': 'LDOS'}
        self._attributes = ['Section_parameters']


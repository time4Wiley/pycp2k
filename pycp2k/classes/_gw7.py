from pycp2k.inputsection import InputSection
from ._print103 import _print103


class _gw7(InputSection):
    def __init__(self):
        InputSection.__init__(self)
        self.Section_parameters = None
        self.Num_time_freq_points = None
        self.Eps_filter = None
        self.Memory_per_proc = None
        self.Approx_kp_extrapol = None
        self.PRINT = _print103()
        self._name = "GW"
        self._keywords = {'Num_time_freq_points': 'NUM_TIME_FREQ_POINTS', 'Eps_filter': 'EPS_FILTER', 'Memory_per_proc': 'MEMORY_PER_PROC', 'Approx_kp_extrapol': 'APPROX_KP_EXTRAPOL'}
        self._subsections = {'PRINT': 'PRINT'}
        self._attributes = ['Section_parameters']


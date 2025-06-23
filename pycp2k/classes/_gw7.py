from pycp2k.inputsection import InputSection
from ._print115 import _print115


class _gw7(InputSection):
    def __init__(self):
        InputSection.__init__(self)
        self.Section_parameters = None
        self.Num_time_freq_points = None
        self.Eps_filter = None
        self.Regularization_ri = None
        self.Cutoff_radius_ri = None
        self.Memory_per_proc = None
        self.Approx_kp_extrapol = None
        self.Size_lattice_sum = None
        self.Kpoints_w = None
        self.Hedin_shift = None
        self.PRINT = _print115()
        self._name = "GW"
        self._keywords = {'Num_time_freq_points': 'NUM_TIME_FREQ_POINTS', 'Eps_filter': 'EPS_FILTER', 'Regularization_ri': 'REGULARIZATION_RI', 'Cutoff_radius_ri': 'CUTOFF_RADIUS_RI', 'Memory_per_proc': 'MEMORY_PER_PROC', 'Approx_kp_extrapol': 'APPROX_KP_EXTRAPOL', 'Size_lattice_sum': 'SIZE_LATTICE_SUM', 'Kpoints_w': 'KPOINTS_W', 'Hedin_shift': 'HEDIN_SHIFT'}
        self._subsections = {'PRINT': 'PRINT'}
        self._attributes = ['Section_parameters']


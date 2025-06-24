from pycp2k.inputsection import InputSection
from ._print66 import _print66


class _real_time_propagation1(InputSection):
    def __init__(self):
        InputSection.__init__(self)
        self.Max_iter = None
        self.Eps_iter = None
        self.Aspc_order = None
        self.Mat_exp = None
        self.Density_propagation = None
        self.Sc_check_start = None
        self.Exp_accuracy = None
        self.Propagator = None
        self.Initial_wfn = None
        self.Apply_delta_pulse = None
        self.Apply_delta_pulse_mag = None
        self.Velocity_gauge = None
        self.Gauge_orig = None
        self.Gauge_orig_manual = None
        self.Vg_com_nl = None
        self.Com_nl = None
        self.Len_rep = None
        self.Periodic = None
        self.Delta_pulse_direction = None
        self.Delta_pulse_scale = None
        self.Hfx_balance_in_core = None
        self.Mcweeny_max_iter = None
        self.Accuracy_refinement = None
        self.Mcweeny_eps = None
        self.PRINT = _print66()
        self._name = "REAL_TIME_PROPAGATION"
        self._keywords = {'Max_iter': 'MAX_ITER', 'Eps_iter': 'EPS_ITER', 'Aspc_order': 'ASPC_ORDER', 'Mat_exp': 'MAT_EXP', 'Density_propagation': 'DENSITY_PROPAGATION', 'Sc_check_start': 'SC_CHECK_START', 'Exp_accuracy': 'EXP_ACCURACY', 'Propagator': 'PROPAGATOR', 'Initial_wfn': 'INITIAL_WFN', 'Apply_delta_pulse': 'APPLY_DELTA_PULSE', 'Apply_delta_pulse_mag': 'APPLY_DELTA_PULSE_MAG', 'Velocity_gauge': 'VELOCITY_GAUGE', 'Gauge_orig': 'GAUGE_ORIG', 'Gauge_orig_manual': 'GAUGE_ORIG_MANUAL', 'Vg_com_nl': 'VG_COM_NL', 'Com_nl': 'COM_NL', 'Len_rep': 'LEN_REP', 'Periodic': 'PERIODIC', 'Delta_pulse_direction': 'DELTA_PULSE_DIRECTION', 'Delta_pulse_scale': 'DELTA_PULSE_SCALE', 'Hfx_balance_in_core': 'HFX_BALANCE_IN_CORE', 'Mcweeny_max_iter': 'MCWEENY_MAX_ITER', 'Accuracy_refinement': 'ACCURACY_REFINEMENT', 'Mcweeny_eps': 'MCWEENY_EPS'}
        self._subsections = {'PRINT': 'PRINT'}


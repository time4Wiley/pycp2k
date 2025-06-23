from pycp2k.inputsection import InputSection


class _excited_states1(InputSection):
    def __init__(self):
        InputSection.__init__(self)
        self.Section_parameters = None
        self.State = None
        self.Xc_kernel_method = None
        self.Eps_delta_rho = None
        self.Diff_order = None
        self.Overlap_deltat = None
        self.Debug_forces = None
        self._name = "EXCITED_STATES"
        self._keywords = {'State': 'STATE', 'Xc_kernel_method': 'XC_KERNEL_METHOD', 'Eps_delta_rho': 'EPS_DELTA_RHO', 'Diff_order': 'DIFF_ORDER', 'Overlap_deltat': 'OVERLAP_DELTAT', 'Debug_forces': 'DEBUG_FORCES'}
        self._attributes = ['Section_parameters']


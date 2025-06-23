from pycp2k.inputsection import InputSection


class _cphf6(InputSection):
    def __init__(self):
        InputSection.__init__(self)
        self.Max_iter = None
        self.Restart_every = None
        self.Solver_method = None
        self.Eps_conv = None
        self.Scale_step_size = None
        self.Enforce_decrease = None
        self.Do_polak_ribiere = None
        self.Recalc_residual = None
        self._name = "CPHF"
        self._keywords = {'Max_iter': 'MAX_ITER', 'Restart_every': 'RESTART_EVERY', 'Solver_method': 'SOLVER_METHOD', 'Eps_conv': 'EPS_CONV', 'Scale_step_size': 'SCALE_STEP_SIZE', 'Enforce_decrease': 'ENFORCE_DECREASE', 'Do_polak_ribiere': 'DO_POLAK_RIBIERE', 'Recalc_residual': 'RECALC_RESIDUAL'}
        self._aliases = {'Max_num_iter': 'Max_iter'}


    @property
    def Max_num_iter(self):
        """
        See documentation for Max_iter
        """
        return self.Max_iter

    @Max_num_iter.setter
    def Max_num_iter(self, value):
        self.Max_iter = value

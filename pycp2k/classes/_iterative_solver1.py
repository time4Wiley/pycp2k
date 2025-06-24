from pycp2k.inputsection import InputSection


class _iterative_solver1(InputSection):
    def __init__(self):
        InputSection.__init__(self)
        self.Converge_by_energy = None
        self.Early_restart = None
        self.Empty_states_tolerance = None
        self.Energy_tolerance = None
        self.Extra_ortho = None
        self.Init_eval_old = None
        self.Init_subspace = None
        self.Locking = None
        self.Min_num_res = None
        self.Num_singular = None
        self.Num_steps = None
        self.Relative_tolerance = None
        self.Residual_tolerance = None
        self.Subspace_size = None
        self.Type = None
        self._name = "ITERATIVE_SOLVER"
        self._keywords = {'Converge_by_energy': 'CONVERGE_BY_ENERGY', 'Early_restart': 'EARLY_RESTART', 'Empty_states_tolerance': 'EMPTY_STATES_TOLERANCE', 'Energy_tolerance': 'ENERGY_TOLERANCE', 'Extra_ortho': 'EXTRA_ORTHO', 'Init_eval_old': 'INIT_EVAL_OLD', 'Init_subspace': 'INIT_SUBSPACE', 'Locking': 'LOCKING', 'Min_num_res': 'MIN_NUM_RES', 'Num_singular': 'NUM_SINGULAR', 'Num_steps': 'NUM_STEPS', 'Relative_tolerance': 'RELATIVE_TOLERANCE', 'Residual_tolerance': 'RESIDUAL_TOLERANCE', 'Subspace_size': 'SUBSPACE_SIZE', 'Type': 'TYPE'}


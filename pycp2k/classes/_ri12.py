from pycp2k.inputsection import InputSection
from ._print51 import _print51


class _ri12(InputSection):
    def __init__(self):
        InputSection.__init__(self)
        self.Section_parameters = None
        self.Eps_filter = None
        self.Eps_filter_2c = None
        self.Eps_storage_scaling = None
        self.Eps_filter_mo = None
        self.Omega = None
        self.Cutoff_radius = None
        self.Kp_ngroups = None
        self.Kp_use_delta_p = None
        self.Kp_stack_size = None
        self.Kp_ri_bump_factor = None
        self.Ri_metric = None
        self.Num2c_matrix_functions = None
        self.Eps_eigval = None
        self.Check_2c_matrix = None
        self.Calc_cond_num = None
        self.Sqrt_order = None
        self.Eps_lanczos = None
        self.Eps_pgf_orb = None
        self.Max_iter_lanczos = None
        self.Ri_flavor = None
        self.Min_block_size = None
        self.Max_block_size_mo = None
        self.Memory_cut = None
        self.Flavor_switch_memory_cut = None
        self.PRINT = _print51()
        self._name = "RI"
        self._keywords = {'Eps_filter': 'EPS_FILTER', 'Eps_filter_2c': 'EPS_FILTER_2C', 'Eps_storage_scaling': 'EPS_STORAGE_SCALING', 'Eps_filter_mo': 'EPS_FILTER_MO', 'Omega': 'OMEGA', 'Cutoff_radius': 'CUTOFF_RADIUS', 'Kp_ngroups': 'KP_NGROUPS', 'Kp_use_delta_p': 'KP_USE_DELTA_P', 'Kp_stack_size': 'KP_STACK_SIZE', 'Kp_ri_bump_factor': 'KP_RI_BUMP_FACTOR', 'Ri_metric': 'RI_METRIC', 'Num2c_matrix_functions': '2C_MATRIX_FUNCTIONS', 'Eps_eigval': 'EPS_EIGVAL', 'Check_2c_matrix': 'CHECK_2C_MATRIX', 'Calc_cond_num': 'CALC_COND_NUM', 'Sqrt_order': 'SQRT_ORDER', 'Eps_lanczos': 'EPS_LANCZOS', 'Eps_pgf_orb': 'EPS_PGF_ORB', 'Max_iter_lanczos': 'MAX_ITER_LANCZOS', 'Ri_flavor': 'RI_FLAVOR', 'Min_block_size': 'MIN_BLOCK_SIZE', 'Max_block_size_mo': 'MAX_BLOCK_SIZE_MO', 'Memory_cut': 'MEMORY_CUT', 'Flavor_switch_memory_cut': 'FLAVOR_SWITCH_MEMORY_CUT'}
        self._subsections = {'PRINT': 'PRINT'}
        self._aliases = {'Kp_eps_filter': 'Eps_filter', 'Kp_omega': 'Omega', 'Kp_cutoff_radius': 'Cutoff_radius', 'Ngroups': 'Kp_ngroups', 'Use_delta_p': 'Kp_use_delta_p', 'Kp_use_p_diff': 'Kp_use_delta_p', 'Use_p_diff': 'Kp_use_delta_p', 'Stack_size': 'Kp_stack_size', 'Ri_bump': 'Kp_ri_bump_factor', 'Bump': 'Kp_ri_bump_factor', 'Bump_factor': 'Kp_ri_bump_factor', 'Kp_ri_metric': 'Ri_metric', 'Calc_condition_number': 'Calc_cond_num', 'Kp_eps_pgf_orb': 'Eps_pgf_orb'}
        self._attributes = ['Section_parameters']


    @property
    def Kp_eps_filter(self):
        """
        See documentation for Eps_filter
        """
        return self.Eps_filter

    @property
    def Kp_omega(self):
        """
        See documentation for Omega
        """
        return self.Omega

    @property
    def Kp_cutoff_radius(self):
        """
        See documentation for Cutoff_radius
        """
        return self.Cutoff_radius

    @property
    def Ngroups(self):
        """
        See documentation for Kp_ngroups
        """
        return self.Kp_ngroups

    @property
    def Use_delta_p(self):
        """
        See documentation for Kp_use_delta_p
        """
        return self.Kp_use_delta_p

    @property
    def Kp_use_p_diff(self):
        """
        See documentation for Kp_use_delta_p
        """
        return self.Kp_use_delta_p

    @property
    def Use_p_diff(self):
        """
        See documentation for Kp_use_delta_p
        """
        return self.Kp_use_delta_p

    @property
    def Stack_size(self):
        """
        See documentation for Kp_stack_size
        """
        return self.Kp_stack_size

    @property
    def Ri_bump(self):
        """
        See documentation for Kp_ri_bump_factor
        """
        return self.Kp_ri_bump_factor

    @property
    def Bump(self):
        """
        See documentation for Kp_ri_bump_factor
        """
        return self.Kp_ri_bump_factor

    @property
    def Bump_factor(self):
        """
        See documentation for Kp_ri_bump_factor
        """
        return self.Kp_ri_bump_factor

    @property
    def Kp_ri_metric(self):
        """
        See documentation for Ri_metric
        """
        return self.Ri_metric

    @property
    def Calc_condition_number(self):
        """
        See documentation for Calc_cond_num
        """
        return self.Calc_cond_num

    @property
    def Kp_eps_pgf_orb(self):
        """
        See documentation for Eps_pgf_orb
        """
        return self.Eps_pgf_orb

    @Kp_eps_filter.setter
    def Kp_eps_filter(self, value):
        self.Eps_filter = value

    @Kp_omega.setter
    def Kp_omega(self, value):
        self.Omega = value

    @Kp_cutoff_radius.setter
    def Kp_cutoff_radius(self, value):
        self.Cutoff_radius = value

    @Ngroups.setter
    def Ngroups(self, value):
        self.Kp_ngroups = value

    @Use_delta_p.setter
    def Use_delta_p(self, value):
        self.Kp_use_delta_p = value

    @Kp_use_p_diff.setter
    def Kp_use_p_diff(self, value):
        self.Kp_use_delta_p = value

    @Use_p_diff.setter
    def Use_p_diff(self, value):
        self.Kp_use_delta_p = value

    @Stack_size.setter
    def Stack_size(self, value):
        self.Kp_stack_size = value

    @Ri_bump.setter
    def Ri_bump(self, value):
        self.Kp_ri_bump_factor = value

    @Bump.setter
    def Bump(self, value):
        self.Kp_ri_bump_factor = value

    @Bump_factor.setter
    def Bump_factor(self, value):
        self.Kp_ri_bump_factor = value

    @Kp_ri_metric.setter
    def Kp_ri_metric(self, value):
        self.Ri_metric = value

    @Calc_condition_number.setter
    def Calc_condition_number(self, value):
        self.Calc_cond_num = value

    @Kp_eps_pgf_orb.setter
    def Kp_eps_pgf_orb(self, value):
        self.Eps_pgf_orb = value

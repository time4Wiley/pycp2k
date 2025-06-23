from pycp2k.inputsection import InputSection
from ._cphf1 import _cphf1


class _low_scaling1(InputSection):
    def __init__(self):
        InputSection.__init__(self)
        self.Section_parameters = None
        self.Memory_cut = None
        self.Memory_info = None
        self.Eps_filter = None
        self.Eps_filter_factor = None
        self.Eps_storage_scaling = None
        self.Do_kpoints = None
        self.Kpoints = None
        self.Kpoint_weights_w = None
        self.Exponent_tailored_weights = None
        self.Regularization_ri = None
        self.Eps_eigval_s = None
        self.Eps_eigval_s_gamma = None
        self.Make_chi_pos_definite = None
        self.Make_overlap_mat_ao_pos_definite = None
        self.Do_extrapolate_kpoints = None
        self.Trunc_coulomb_ri_x = None
        self.Rel_cutoff_trunc_coulomb_ri_x = None
        self.Keep_quadrature = None
        self.K_mesh_g_factor = None
        self.Min_block_size = None
        self.Min_block_size_mo = None
        self.CPHF = _cphf1()
        self._name = "LOW_SCALING"
        self._keywords = {'Memory_cut': 'MEMORY_CUT', 'Memory_info': 'MEMORY_INFO', 'Eps_filter': 'EPS_FILTER', 'Eps_filter_factor': 'EPS_FILTER_FACTOR', 'Eps_storage_scaling': 'EPS_STORAGE_SCALING', 'Do_kpoints': 'DO_KPOINTS', 'Kpoints': 'KPOINTS', 'Kpoint_weights_w': 'KPOINT_WEIGHTS_W', 'Exponent_tailored_weights': 'EXPONENT_TAILORED_WEIGHTS', 'Regularization_ri': 'REGULARIZATION_RI', 'Eps_eigval_s': 'EPS_EIGVAL_S', 'Eps_eigval_s_gamma': 'EPS_EIGVAL_S_GAMMA', 'Make_chi_pos_definite': 'MAKE_CHI_POS_DEFINITE', 'Make_overlap_mat_ao_pos_definite': 'MAKE_OVERLAP_MAT_AO_POS_DEFINITE', 'Do_extrapolate_kpoints': 'DO_EXTRAPOLATE_KPOINTS', 'Trunc_coulomb_ri_x': 'TRUNC_COULOMB_RI_X', 'Rel_cutoff_trunc_coulomb_ri_x': 'REL_CUTOFF_TRUNC_COULOMB_RI_X', 'Keep_quadrature': 'KEEP_QUADRATURE', 'K_mesh_g_factor': 'K_MESH_G_FACTOR', 'Min_block_size': 'MIN_BLOCK_SIZE', 'Min_block_size_mo': 'MIN_BLOCK_SIZE_MO'}
        self._subsections = {'CPHF': 'CPHF'}
        self._aliases = {'Eps_storage': 'Eps_storage_scaling', 'Keep_weights': 'Keep_quadrature', 'Keep_quad': 'Keep_quadrature', 'Keep_weight': 'Keep_quadrature'}
        self._attributes = ['Section_parameters']


    @property
    def Eps_storage(self):
        """
        See documentation for Eps_storage_scaling
        """
        return self.Eps_storage_scaling

    @property
    def Keep_weights(self):
        """
        See documentation for Keep_quadrature
        """
        return self.Keep_quadrature

    @property
    def Keep_quad(self):
        """
        See documentation for Keep_quadrature
        """
        return self.Keep_quadrature

    @property
    def Keep_weight(self):
        """
        See documentation for Keep_quadrature
        """
        return self.Keep_quadrature

    @Eps_storage.setter
    def Eps_storage(self, value):
        self.Eps_storage_scaling = value

    @Keep_weights.setter
    def Keep_weights(self, value):
        self.Keep_quadrature = value

    @Keep_quad.setter
    def Keep_quad(self, value):
        self.Keep_quadrature = value

    @Keep_weight.setter
    def Keep_weight(self, value):
        self.Keep_quadrature = value

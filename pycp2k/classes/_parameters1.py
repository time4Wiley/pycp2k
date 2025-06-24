from pycp2k.inputsection import InputSection


class _parameters1(InputSection):
    def __init__(self):
        InputSection.__init__(self)
        self.Vdw_functional = None
        self.Auto_rmt = None
        self.Aw_cutoff = None
        self.Core_relativity = None
        self.Density_tol = None
        self.Electronic_structure_method = None
        self.Energy_tol = None
        self.Extra_charge = None
        self.Gamma_point = None
        self.Gk_cutoff = None
        self.Hubbard_correction = None
        self.Lmax_apw = None
        self.Lmax_pot = None
        self.Lmax_rho = None
        self.Molecule = None
        self.Ngridk = None
        self.Nn_radius = None
        self.Num_bands = None
        self.Num_dft_iter = None
        self.Num_fv_states = None
        self.Num_mag_dims = None
        self.Precision_gs = None
        self.Precision_hs = None
        self.Precision_wf = None
        self.Pw_cutoff = None
        self.Reduce_aux_bf = None
        self.Shiftk = None
        self.Smearing = None
        self.Smearing_width = None
        self.So_correction = None
        self.Use_ibz = None
        self.Use_scf_correction = None
        self.Use_symmetry = None
        self.Valence_relativity = None
        self.Xc_dens_tre = None
        self._name = "PARAMETERS"
        self._keywords = {'Vdw_functional': 'VDW_FUNCTIONAL', 'Auto_rmt': 'AUTO_RMT', 'Aw_cutoff': 'AW_CUTOFF', 'Core_relativity': 'CORE_RELATIVITY', 'Density_tol': 'DENSITY_TOL', 'Electronic_structure_method': 'ELECTRONIC_STRUCTURE_METHOD', 'Energy_tol': 'ENERGY_TOL', 'Extra_charge': 'EXTRA_CHARGE', 'Gamma_point': 'GAMMA_POINT', 'Gk_cutoff': 'GK_CUTOFF', 'Hubbard_correction': 'HUBBARD_CORRECTION', 'Lmax_apw': 'LMAX_APW', 'Lmax_pot': 'LMAX_POT', 'Lmax_rho': 'LMAX_RHO', 'Molecule': 'MOLECULE', 'Ngridk': 'NGRIDK', 'Nn_radius': 'NN_RADIUS', 'Num_bands': 'NUM_BANDS', 'Num_dft_iter': 'NUM_DFT_ITER', 'Num_fv_states': 'NUM_FV_STATES', 'Num_mag_dims': 'NUM_MAG_DIMS', 'Precision_gs': 'PRECISION_GS', 'Precision_hs': 'PRECISION_HS', 'Precision_wf': 'PRECISION_WF', 'Pw_cutoff': 'PW_CUTOFF', 'Reduce_aux_bf': 'REDUCE_AUX_BF', 'Shiftk': 'SHIFTK', 'Smearing': 'SMEARING', 'Smearing_width': 'SMEARING_WIDTH', 'So_correction': 'SO_CORRECTION', 'Use_ibz': 'USE_IBZ', 'Use_scf_correction': 'USE_SCF_CORRECTION', 'Use_symmetry': 'USE_SYMMETRY', 'Valence_relativity': 'VALENCE_RELATIVITY', 'Xc_dens_tre': 'XC_DENS_TRE'}


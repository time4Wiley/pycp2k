from pycp2k.inputsection import InputSection


class _parameter2(InputSection):
    def __init__(self):
        InputSection.__init__(self)
        self.Param_file_path = None
        self.Param_file_name = None
        self.Dispersion_parameter_file = None
        self.Dispersion_radius = None
        self.Coordination_cutoff = None
        self.D3bj_scaling = None
        self.D3bj_param = None
        self.Huckel_constants = None
        self.Coulomb_constants = None
        self.Cn_constants = None
        self.En_constants = None
        self.Ben_constant = None
        self.Enscale = None
        self.Halogen_binding = None
        self.Kab_param = []
        self.Xb_radius = None
        self.Coulomb_sr_cut = None
        self.Coulomb_sr_eps = None
        self.Srb_parameter = None
        self._name = "PARAMETER"
        self._keywords = {'Param_file_path': 'PARAM_FILE_PATH', 'Param_file_name': 'PARAM_FILE_NAME', 'Dispersion_parameter_file': 'DISPERSION_PARAMETER_FILE', 'Dispersion_radius': 'DISPERSION_RADIUS', 'Coordination_cutoff': 'COORDINATION_CUTOFF', 'D3bj_scaling': 'D3BJ_SCALING', 'D3bj_param': 'D3BJ_PARAM', 'Huckel_constants': 'HUCKEL_CONSTANTS', 'Coulomb_constants': 'COULOMB_CONSTANTS', 'Cn_constants': 'CN_CONSTANTS', 'En_constants': 'EN_CONSTANTS', 'Ben_constant': 'BEN_CONSTANT', 'Enscale': 'ENSCALE', 'Halogen_binding': 'HALOGEN_BINDING', 'Xb_radius': 'XB_RADIUS', 'Coulomb_sr_cut': 'COULOMB_SR_CUT', 'Coulomb_sr_eps': 'COULOMB_SR_EPS', 'Srb_parameter': 'SRB_PARAMETER'}
        self._repeated_keywords = {'Kab_param': 'KAB_PARAM'}


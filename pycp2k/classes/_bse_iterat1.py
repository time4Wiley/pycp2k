from pycp2k.inputsection import InputSection


class _bse_iterat1(InputSection):
    def __init__(self):
        InputSection.__init__(self)
        self.Davidson_abort_cond = None
        self.Num_exc_en = None
        self.Num_add_start_z_space = None
        self.Fac_max_z_space = None
        self.Num_new_t = None
        self.Eps_res = None
        self.Eps_exc_en = None
        self.Num_davidson_iter = None
        self.Z_space_energy_cutoff = None
        self._name = "BSE_ITERAT"
        self._keywords = {'Davidson_abort_cond': 'DAVIDSON_ABORT_COND', 'Num_exc_en': 'NUM_EXC_EN', 'Num_add_start_z_space': 'NUM_ADD_START_Z_SPACE', 'Fac_max_z_space': 'FAC_MAX_Z_SPACE', 'Num_new_t': 'NUM_NEW_T', 'Eps_res': 'EPS_RES', 'Eps_exc_en': 'EPS_EXC_EN', 'Num_davidson_iter': 'NUM_DAVIDSON_ITER', 'Z_space_energy_cutoff': 'Z_SPACE_ENERGY_CUTOFF'}


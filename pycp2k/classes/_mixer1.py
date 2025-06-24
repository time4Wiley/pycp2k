from pycp2k.inputsection import InputSection


class _mixer1(InputSection):
    def __init__(self):
        InputSection.__init__(self)
        self.Beta = None
        self.Beta0 = None
        self.Beta_scaling_factor = None
        self.Linear_mix_rms_tol = None
        self.Max_history = None
        self.Type = None
        self.Use_hartree = None
        self._name = "MIXER"
        self._keywords = {'Beta': 'BETA', 'Beta0': 'BETA0', 'Beta_scaling_factor': 'BETA_SCALING_FACTOR', 'Linear_mix_rms_tol': 'LINEAR_MIX_RMS_TOL', 'Max_history': 'MAX_HISTORY', 'Type': 'TYPE', 'Use_hartree': 'USE_HARTREE'}


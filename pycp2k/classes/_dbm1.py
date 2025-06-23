from pycp2k.inputsection import InputSection


class _dbm1(InputSection):
    def __init__(self):
        InputSection.__init__(self)
        self.N_loop = None
        self.M = None
        self.N = None
        self.K = None
        self.Transa = None
        self.Transb = None
        self.Bs_m = None
        self.Bs_n = None
        self.Bs_k = None
        self.Keepsparse = None
        self.Asparsity = None
        self.Bsparsity = None
        self.Csparsity = None
        self.Alpha = None
        self.Beta = None
        self.Filter_eps = None
        self.Always_checksum = None
        self._name = "DBM"
        self._keywords = {'N_loop': 'N_LOOP', 'M': 'M', 'N': 'N', 'K': 'K', 'Transa': 'TRANSA', 'Transb': 'TRANSB', 'Bs_m': 'BS_M', 'Bs_n': 'BS_N', 'Bs_k': 'BS_K', 'Keepsparse': 'KEEPSPARSE', 'Asparsity': 'ASPARSITY', 'Bsparsity': 'BSPARSITY', 'Csparsity': 'CSPARSITY', 'Alpha': 'ALPHA', 'Beta': 'BETA', 'Filter_eps': 'FILTER_EPS', 'Always_checksum': 'ALWAYS_CHECKSUM'}


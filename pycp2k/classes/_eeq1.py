from pycp2k.inputsection import InputSection


class _eeq1(InputSection):
    def __init__(self):
        InputSection.__init__(self)
        self.Direct = None
        self.Sparse = None
        self.Eps_diis = None
        self.Alpha = None
        self.Max_diis = None
        self.Mdiis = None
        self.Sdiis = None
        self._name = "EEQ"
        self._keywords = {'Direct': 'DIRECT', 'Sparse': 'SPARSE', 'Eps_diis': 'EPS_DIIS', 'Alpha': 'ALPHA', 'Max_diis': 'MAX_DIIS', 'Mdiis': 'MDIIS', 'Sdiis': 'SDIIS'}


from pycp2k.inputsection import InputSection


class _cphf3(InputSection):
    def __init__(self):
        InputSection.__init__(self)
        self.Eps_conv = None
        self.Max_iter = None
        self.Preconditioner = None
        self.Energy_gap = None
        self._name = "CPHF"
        self._keywords = {'Eps_conv': 'EPS_CONV', 'Max_iter': 'MAX_ITER', 'Preconditioner': 'PRECONDITIONER', 'Energy_gap': 'ENERGY_GAP'}


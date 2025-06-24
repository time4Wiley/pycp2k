from pycp2k.inputsection import InputSection


class _linres2(InputSection):
    def __init__(self):
        InputSection.__init__(self)
        self.Eps = None
        self.Eps_filter = None
        self.Max_iter = None
        self.Restart_every = None
        self.Preconditioner = None
        self.Energy_gap = None
        self.Restart = None
        self.Wfn_restart_file_name = None
        self._name = "LINRES"
        self._keywords = {'Eps': 'EPS', 'Eps_filter': 'EPS_FILTER', 'Max_iter': 'MAX_ITER', 'Restart_every': 'RESTART_EVERY', 'Preconditioner': 'PRECONDITIONER', 'Energy_gap': 'ENERGY_GAP', 'Restart': 'RESTART', 'Wfn_restart_file_name': 'WFN_RESTART_FILE_NAME'}
        self._aliases = {'Restart_file_name': 'Wfn_restart_file_name'}


    @property
    def Restart_file_name(self):
        """
        See documentation for Wfn_restart_file_name
        """
        return self.Wfn_restart_file_name

    @Restart_file_name.setter
    def Restart_file_name(self, value):
        self.Wfn_restart_file_name = value

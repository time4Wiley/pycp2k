from pycp2k.inputsection import InputSection


class _soc1(InputSection):
    def __init__(self):
        InputSection.__init__(self)
        self.Eps_filter = None
        self.Grid = []
        self.Atomic_grid = self.Grid
        self._name = "SOC"
        self._keywords = {'Eps_filter': 'EPS_FILTER'}
        self._repeated_keywords = {'Grid': 'GRID'}
        self._aliases = {'Eps_filter_matrix': 'Eps_filter'}
        self._repeated_aliases = {'Atomic_grid': 'Grid'}


    @property
    def Eps_filter_matrix(self):
        """
        See documentation for Eps_filter
        """
        return self.Eps_filter

    @Eps_filter_matrix.setter
    def Eps_filter_matrix(self, value):
        self.Eps_filter = value

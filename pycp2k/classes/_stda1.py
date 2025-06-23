from pycp2k.inputsection import InputSection


class _stda1(InputSection):
    def __init__(self):
        InputSection.__init__(self)
        self.Fraction = None
        self.Do_exchange = None
        self.Do_ewald = None
        self.Eps_td_filter = None
        self.Mataga_nishimoto_cexp = None
        self.Mataga_nishimoto_xexp = None
        self.Coulomb_sr_cut = None
        self.Coulomb_sr_eps = None
        self._name = "STDA"
        self._keywords = {'Fraction': 'FRACTION', 'Do_exchange': 'DO_EXCHANGE', 'Do_ewald': 'DO_EWALD', 'Eps_td_filter': 'EPS_TD_FILTER', 'Mataga_nishimoto_cexp': 'MATAGA_NISHIMOTO_CEXP', 'Mataga_nishimoto_xexp': 'MATAGA_NISHIMOTO_XEXP', 'Coulomb_sr_cut': 'COULOMB_SR_CUT', 'Coulomb_sr_eps': 'COULOMB_SR_EPS'}
        self._aliases = {'Hfx_fraction': 'Fraction'}


    @property
    def Hfx_fraction(self):
        """
        See documentation for Fraction
        """
        return self.Fraction

    @Hfx_fraction.setter
    def Hfx_fraction(self, value):
        self.Fraction = value

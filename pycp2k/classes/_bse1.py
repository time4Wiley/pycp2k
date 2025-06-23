from pycp2k.inputsection import InputSection
from ._screening_in_w1 import _screening_in_w1
from ._bse_iterat1 import _bse_iterat1
from ._bse_spectrum1 import _bse_spectrum1
from ._nto_analysis1 import _nto_analysis1


class _bse1(InputSection):
    def __init__(self):
        InputSection.__init__(self)
        self.Section_parameters = None
        self.Spin_config = None
        self.Bse_diag_method = None
        self.Tda = None
        self.Energy_cutoff_occ = None
        self.Energy_cutoff_empty = None
        self.Bse_debug_print = None
        self.Num_print_exc = None
        self.Num_print_exc_descr = None
        self.Print_directional_exc_descr = None
        self.Eps_x = None
        self.Use_ks_energies = None
        self.SCREENING_IN_W = _screening_in_w1()
        self.BSE_ITERAT = _bse_iterat1()
        self.BSE_SPECTRUM = _bse_spectrum1()
        self.NTO_ANALYSIS = _nto_analysis1()
        self._name = "BSE"
        self._keywords = {'Spin_config': 'SPIN_CONFIG', 'Bse_diag_method': 'BSE_DIAG_METHOD', 'Tda': 'TDA', 'Energy_cutoff_occ': 'ENERGY_CUTOFF_OCC', 'Energy_cutoff_empty': 'ENERGY_CUTOFF_EMPTY', 'Bse_debug_print': 'BSE_DEBUG_PRINT', 'Num_print_exc': 'NUM_PRINT_EXC', 'Num_print_exc_descr': 'NUM_PRINT_EXC_DESCR', 'Print_directional_exc_descr': 'PRINT_DIRECTIONAL_EXC_DESCR', 'Eps_x': 'EPS_X', 'Use_ks_energies': 'USE_KS_ENERGIES'}
        self._subsections = {'SCREENING_IN_W': 'SCREENING_IN_W', 'BSE_ITERAT': 'BSE_ITERAT', 'BSE_SPECTRUM': 'BSE_SPECTRUM', 'NTO_ANALYSIS': 'NTO_ANALYSIS'}
        self._attributes = ['Section_parameters']


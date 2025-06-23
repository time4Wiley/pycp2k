from pycp2k.inputsection import InputSection
from ._hf5 import _hf5
from ._gw2 import _gw2
from ._exchange_correction2 import _exchange_correction2


class _ri_rpa2(InputSection):
    def __init__(self):
        InputSection.__init__(self)
        self.Section_parameters = None
        self.Sigma_functional = None
        self.Quadrature_points = None
        self.Num_integ_groups = None
        self.Mm_style = None
        self.Minimax_quadrature = None
        self.Rse = None
        self.Admm = None
        self.Scale_rpa = None
        self.Print_dgemm_info = None
        self.HF_list = []
        self.GW = _gw2()
        self.EXCHANGE_CORRECTION = _exchange_correction2()
        self._name = "RI_RPA"
        self._keywords = {'Sigma_functional': 'SIGMA_FUNCTIONAL', 'Quadrature_points': 'QUADRATURE_POINTS', 'Num_integ_groups': 'NUM_INTEG_GROUPS', 'Mm_style': 'MM_STYLE', 'Minimax_quadrature': 'MINIMAX_QUADRATURE', 'Rse': 'RSE', 'Admm': 'ADMM', 'Scale_rpa': 'SCALE_RPA', 'Print_dgemm_info': 'PRINT_DGEMM_INFO'}
        self._subsections = {'GW': 'GW', 'EXCHANGE_CORRECTION': 'EXCHANGE_CORRECTION'}
        self._repeated_subsections = {'HF': '_hf5'}
        self._aliases = {'Rpa_num_quad_points': 'Quadrature_points', 'Minimax': 'Minimax_quadrature', 'Se': 'Rse'}
        self._attributes = ['Section_parameters', 'HF_list']

    def HF_add(self, section_parameters=None):
        new_section = _hf5()
        if section_parameters is not None:
            if hasattr(new_section, 'Section_parameters'):
                new_section.Section_parameters = section_parameters
        self.HF_list.append(new_section)
        return new_section


    @property
    def Rpa_num_quad_points(self):
        """
        See documentation for Quadrature_points
        """
        return self.Quadrature_points

    @property
    def Minimax(self):
        """
        See documentation for Minimax_quadrature
        """
        return self.Minimax_quadrature

    @property
    def Se(self):
        """
        See documentation for Rse
        """
        return self.Rse

    @Rpa_num_quad_points.setter
    def Rpa_num_quad_points(self, value):
        self.Quadrature_points = value

    @Minimax.setter
    def Minimax(self, value):
        self.Minimax_quadrature = value

    @Se.setter
    def Se(self, value):
        self.Rse = value

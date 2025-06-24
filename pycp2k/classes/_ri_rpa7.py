from pycp2k.inputsection import InputSection
from ._hf14 import _hf14
from ._gw8 import _gw8
from ._ri_axk7 import _ri_axk7


class _ri_rpa7(InputSection):
    def __init__(self):
        InputSection.__init__(self)
        self.Section_parameters = None
        self.Quadrature_points = None
        self.Num_integ_groups = None
        self.Mm_style = None
        self.Minimax_quadrature = None
        self.Ri_axk = None
        self.Rse = None
        self.Admm = None
        self.Scale_rpa = None
        self.Print_dgemm_info = None
        self.HF_list = []
        self.GW = _gw8()
        self.RI_AXK = _ri_axk7()
        self._name = "RI_RPA"
        self._keywords = {'Quadrature_points': 'QUADRATURE_POINTS', 'Num_integ_groups': 'NUM_INTEG_GROUPS', 'Mm_style': 'MM_STYLE', 'Minimax_quadrature': 'MINIMAX_QUADRATURE', 'Ri_axk': 'RI_AXK', 'Rse': 'RSE', 'Admm': 'ADMM', 'Scale_rpa': 'SCALE_RPA', 'Print_dgemm_info': 'PRINT_DGEMM_INFO'}
        self._subsections = {'GW': 'GW', 'RI_AXK': 'RI_AXK'}
        self._repeated_subsections = {'HF': '_hf14'}
        self._aliases = {'Rpa_num_quad_points': 'Quadrature_points', 'Minimax': 'Minimax_quadrature', 'Axk': 'Ri_axk', 'Se': 'Rse'}
        self._attributes = ['Section_parameters', 'HF_list']

    def HF_add(self, section_parameters=None):
        new_section = _hf14()
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
    def Axk(self):
        """
        See documentation for Ri_axk
        """
        return self.Ri_axk

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

    @Axk.setter
    def Axk(self, value):
        self.Ri_axk = value

    @Se.setter
    def Se(self, value):
        self.Rse = value

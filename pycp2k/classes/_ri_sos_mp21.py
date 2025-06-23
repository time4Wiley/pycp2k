from pycp2k.inputsection import InputSection


class _ri_sos_mp21(InputSection):
    def __init__(self):
        InputSection.__init__(self)
        self.Section_parameters = None
        self.Quadrature_points = None
        self.Num_integ_groups = None
        self._name = "RI_SOS_MP2"
        self._keywords = {'Quadrature_points': 'QUADRATURE_POINTS', 'Num_integ_groups': 'NUM_INTEG_GROUPS'}
        self._aliases = {'Laplace_num_quad_points': 'Quadrature_points'}
        self._attributes = ['Section_parameters']


    @property
    def Laplace_num_quad_points(self):
        """
        See documentation for Quadrature_points
        """
        return self.Quadrature_points

    @Laplace_num_quad_points.setter
    def Laplace_num_quad_points(self, value):
        self.Quadrature_points = value

from pycp2k.inputsection import InputSection
from ._each135 import _each135


class _ri_density_coeffs1(InputSection):
    def __init__(self):
        InputSection.__init__(self)
        self.Section_parameters = None
        self.Add_last = None
        self.Common_iteration_levels = None
        self.Filename = None
        self.Log_print_key = None
        self.Multiply_by_ri_2c_integrals = None
        self.EACH = _each135()
        self._name = "RI_DENSITY_COEFFS"
        self._keywords = {'Add_last': 'ADD_LAST', 'Common_iteration_levels': 'COMMON_ITERATION_LEVELS', 'Filename': 'FILENAME', 'Log_print_key': 'LOG_PRINT_KEY', 'Multiply_by_ri_2c_integrals': 'MULTIPLY_BY_RI_2C_INTEGRALS'}
        self._subsections = {'EACH': 'EACH'}
        self._aliases = {'Mult_by_ri': 'Multiply_by_ri_2c_integrals', 'Mult_by_s': 'Multiply_by_ri_2c_integrals', 'Mult_by_ri_ints': 'Multiply_by_ri_2c_integrals'}
        self._attributes = ['Section_parameters']


    @property
    def Mult_by_ri(self):
        """
        See documentation for Multiply_by_ri_2c_integrals
        """
        return self.Multiply_by_ri_2c_integrals

    @property
    def Mult_by_s(self):
        """
        See documentation for Multiply_by_ri_2c_integrals
        """
        return self.Multiply_by_ri_2c_integrals

    @property
    def Mult_by_ri_ints(self):
        """
        See documentation for Multiply_by_ri_2c_integrals
        """
        return self.Multiply_by_ri_2c_integrals

    @Mult_by_ri.setter
    def Mult_by_ri(self, value):
        self.Multiply_by_ri_2c_integrals = value

    @Mult_by_s.setter
    def Mult_by_s(self, value):
        self.Multiply_by_ri_2c_integrals = value

    @Mult_by_ri_ints.setter
    def Mult_by_ri_ints(self, value):
        self.Multiply_by_ri_2c_integrals = value

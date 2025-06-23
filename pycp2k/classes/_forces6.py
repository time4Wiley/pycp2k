from pycp2k.inputsection import InputSection
from ._each554 import _each554


class _forces6(InputSection):
    def __init__(self):
        InputSection.__init__(self)
        self.Section_parameters = None
        self.Add_last = None
        self.Common_iteration_levels = None
        self.Filename = None
        self.Log_print_key = None
        self.Ndigits = None
        self.Force_unit = None
        self.EACH = _each554()
        self._name = "FORCES"
        self._keywords = {'Add_last': 'ADD_LAST', 'Common_iteration_levels': 'COMMON_ITERATION_LEVELS', 'Filename': 'FILENAME', 'Log_print_key': 'LOG_PRINT_KEY', 'Ndigits': 'NDIGITS', 'Force_unit': 'FORCE_UNIT'}
        self._subsections = {'EACH': 'EACH'}
        self._aliases = {'Unit': 'Force_unit'}
        self._attributes = ['Section_parameters']


    @property
    def Unit(self):
        """
        See documentation for Force_unit
        """
        return self.Force_unit

    @Unit.setter
    def Unit(self, value):
        self.Force_unit = value

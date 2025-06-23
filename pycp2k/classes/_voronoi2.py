from pycp2k.inputsection import InputSection
from ._each319 import _each319


class _voronoi2(InputSection):
    def __init__(self):
        InputSection.__init__(self)
        self.Section_parameters = None
        self.Add_last = None
        self.Common_iteration_levels = None
        self.Filename = None
        self.Log_print_key = None
        self.Append = None
        self.Sanity_check = None
        self.Overwrite = None
        self.Skip_first = None
        self.Verbose = None
        self.Output_emp = None
        self.Output_text = None
        self.Refinement_factor = None
        self.Voronoi_radii = None
        self.User_radii = None
        self.Molecular_properties = None
        self.Molprop_file_name = None
        self.Jitter = None
        self.Jitter_seed = None
        self.Jitter_amplitude = None
        self.EACH = _each319()
        self._name = "VORONOI"
        self._keywords = {'Add_last': 'ADD_LAST', 'Common_iteration_levels': 'COMMON_ITERATION_LEVELS', 'Filename': 'FILENAME', 'Log_print_key': 'LOG_PRINT_KEY', 'Append': 'APPEND', 'Sanity_check': 'SANITY_CHECK', 'Overwrite': 'OVERWRITE', 'Skip_first': 'SKIP_FIRST', 'Verbose': 'VERBOSE', 'Output_emp': 'OUTPUT_EMP', 'Output_text': 'OUTPUT_TEXT', 'Refinement_factor': 'REFINEMENT_FACTOR', 'Voronoi_radii': 'VORONOI_RADII', 'User_radii': 'USER_RADII', 'Molecular_properties': 'MOLECULAR_PROPERTIES', 'Molprop_file_name': 'MOLPROP_FILE_NAME', 'Jitter': 'JITTER', 'Jitter_seed': 'JITTER_SEED', 'Jitter_amplitude': 'JITTER_AMPLITUDE'}
        self._subsections = {'EACH': 'EACH'}
        self._attributes = ['Section_parameters']


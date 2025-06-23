from pycp2k.inputsection import InputSection
from ._sr_cutoff1 import _sr_cutoff1
from ._model1 import _model1
from ._print14 import _print14


class _nnp1(InputSection):
    def __init__(self):
        InputSection.__init__(self)
        self.Nnp_input_file_name = None
        self.Scale_file_name = None
        self.SR_CUTOFF_list = []
        self.MODEL_list = []
        self.PRINT = _print14()
        self._name = "NNP"
        self._keywords = {'Nnp_input_file_name': 'NNP_INPUT_FILE_NAME', 'Scale_file_name': 'SCALE_FILE_NAME'}
        self._subsections = {'PRINT': 'PRINT'}
        self._repeated_subsections = {'SR_CUTOFF': '_sr_cutoff1', 'MODEL': '_model1'}
        self._attributes = ['SR_CUTOFF_list', 'MODEL_list']

    def SR_CUTOFF_add(self, section_parameters=None):
        new_section = _sr_cutoff1()
        if section_parameters is not None:
            if hasattr(new_section, 'Section_parameters'):
                new_section.Section_parameters = section_parameters
        self.SR_CUTOFF_list.append(new_section)
        return new_section

    def MODEL_add(self, section_parameters=None):
        new_section = _model1()
        if section_parameters is not None:
            if hasattr(new_section, 'Section_parameters'):
                new_section.Section_parameters = section_parameters
        self.MODEL_list.append(new_section)
        return new_section


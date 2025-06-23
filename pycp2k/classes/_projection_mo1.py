from pycp2k.inputsection import InputSection
from ._print67 import _print67


class _projection_mo1(InputSection):
    def __init__(self):
        InputSection.__init__(self)
        self.Propagate_ref = None
        self.Reference_type = None
        self.Ref_mo_file_name = None
        self.Ref_mo_index = None
        self.Ref_mo_spin = None
        self.Ref_add_lumo = None
        self.Sum_on_all_ref = None
        self.Td_mo_index = None
        self.Td_mo_spin = None
        self.Sum_on_all_td = None
        self.PRINT = _print67()
        self._name = "PROJECTION_MO"
        self._keywords = {'Propagate_ref': 'PROPAGATE_REF', 'Reference_type': 'REFERENCE_TYPE', 'Ref_mo_file_name': 'REF_MO_FILE_NAME', 'Ref_mo_index': 'REF_MO_INDEX', 'Ref_mo_spin': 'REF_MO_SPIN', 'Ref_add_lumo': 'REF_ADD_LUMO', 'Sum_on_all_ref': 'SUM_ON_ALL_REF', 'Td_mo_index': 'TD_MO_INDEX', 'Td_mo_spin': 'TD_MO_SPIN', 'Sum_on_all_td': 'SUM_ON_ALL_TD'}
        self._subsections = {'PRINT': 'PRINT'}


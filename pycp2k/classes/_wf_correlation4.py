from pycp2k.inputsection import InputSection
from ._mp24 import _mp24
from ._ri_mp24 import _ri_mp24
from ._ri_rpa4 import _ri_rpa4
from ._ri_sos_mp24 import _ri_sos_mp24
from ._low_scaling4 import _low_scaling4
from ._ri15 import _ri15
from ._integrals4 import _integrals4
from ._canonical_gradients4 import _canonical_gradients4
from ._print57 import _print57


class _wf_correlation4(InputSection):
    def __init__(self):
        InputSection.__init__(self)
        self.Memory = None
        self.E_gap = None
        self.E_range = None
        self.Scale_s = None
        self.Scale_t = None
        self.Group_size = None
        self.MP2 = _mp24()
        self.RI_MP2 = _ri_mp24()
        self.RI_RPA = _ri_rpa4()
        self.RI_SOS_MP2 = _ri_sos_mp24()
        self.LOW_SCALING = _low_scaling4()
        self.RI = _ri15()
        self.INTEGRALS = _integrals4()
        self.CANONICAL_GRADIENTS = _canonical_gradients4()
        self.PRINT = _print57()
        self._name = "WF_CORRELATION"
        self._keywords = {'Memory': 'MEMORY', 'E_gap': 'E_GAP', 'E_range': 'E_RANGE', 'Scale_s': 'SCALE_S', 'Scale_t': 'SCALE_T', 'Group_size': 'GROUP_SIZE'}
        self._subsections = {'MP2': 'MP2', 'RI_MP2': 'RI_MP2', 'RI_RPA': 'RI_RPA', 'RI_SOS_MP2': 'RI_SOS_MP2', 'LOW_SCALING': 'LOW_SCALING', 'RI': 'RI', 'INTEGRALS': 'INTEGRALS', 'CANONICAL_GRADIENTS': 'CANONICAL_GRADIENTS', 'PRINT': 'PRINT'}
        self._aliases = {'Number_proc': 'Group_size'}


    @property
    def Number_proc(self):
        """
        See documentation for Group_size
        """
        return self.Group_size

    @Number_proc.setter
    def Number_proc(self, value):
        self.Group_size = value

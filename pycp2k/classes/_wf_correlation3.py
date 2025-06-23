from pycp2k.inputsection import InputSection
from ._mp23 import _mp23
from ._ri_mp23 import _ri_mp23
from ._ri_rpa3 import _ri_rpa3
from ._ri_sos_mp23 import _ri_sos_mp23
from ._low_scaling3 import _low_scaling3
from ._ri11 import _ri11
from ._integrals3 import _integrals3
from ._canonical_gradients3 import _canonical_gradients3
from ._print49 import _print49


class _wf_correlation3(InputSection):
    def __init__(self):
        InputSection.__init__(self)
        self.Memory = None
        self.E_gap = None
        self.E_range = None
        self.Scale_s = None
        self.Scale_t = None
        self.Group_size = None
        self.MP2 = _mp23()
        self.RI_MP2 = _ri_mp23()
        self.RI_RPA = _ri_rpa3()
        self.RI_SOS_MP2 = _ri_sos_mp23()
        self.LOW_SCALING = _low_scaling3()
        self.RI = _ri11()
        self.INTEGRALS = _integrals3()
        self.CANONICAL_GRADIENTS = _canonical_gradients3()
        self.PRINT = _print49()
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

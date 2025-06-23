from pycp2k.inputsection import InputSection
from ._mp22 import _mp22
from ._ri_mp22 import _ri_mp22
from ._ri_rpa2 import _ri_rpa2
from ._ri_sos_mp22 import _ri_sos_mp22
from ._low_scaling2 import _low_scaling2
from ._ri7 import _ri7
from ._integrals2 import _integrals2
from ._canonical_gradients2 import _canonical_gradients2
from ._print39 import _print39


class _wf_correlation2(InputSection):
    def __init__(self):
        InputSection.__init__(self)
        self.Memory = None
        self.E_gap = None
        self.E_range = None
        self.Scale_s = None
        self.Scale_t = None
        self.Group_size = None
        self.MP2 = _mp22()
        self.RI_MP2 = _ri_mp22()
        self.RI_RPA = _ri_rpa2()
        self.RI_SOS_MP2 = _ri_sos_mp22()
        self.LOW_SCALING = _low_scaling2()
        self.RI = _ri7()
        self.INTEGRALS = _integrals2()
        self.CANONICAL_GRADIENTS = _canonical_gradients2()
        self.PRINT = _print39()
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

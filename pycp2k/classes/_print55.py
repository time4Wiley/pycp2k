from pycp2k.inputsection import InputSection
from ._ri_info11 import _ri_info11
from ._ri_density_coeffs11 import _ri_density_coeffs11
from ._ri_metric_2c_ints11 import _ri_metric_2c_ints11


class _print55(InputSection):
    def __init__(self):
        InputSection.__init__(self)
        self.RI_INFO = _ri_info11()
        self.RI_DENSITY_COEFFS = _ri_density_coeffs11()
        self.RI_METRIC_2C_INTS = _ri_metric_2c_ints11()
        self._name = "PRINT"
        self._subsections = {'RI_INFO': 'RI_INFO', 'RI_DENSITY_COEFFS': 'RI_DENSITY_COEFFS', 'RI_METRIC_2C_INTS': 'RI_METRIC_2C_INTS'}


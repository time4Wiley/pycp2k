from pycp2k.inputsection import InputSection
from ._ri_info13 import _ri_info13
from ._ri_density_coeffs13 import _ri_density_coeffs13
from ._ri_metric_2c_ints13 import _ri_metric_2c_ints13


class _print112(InputSection):
    def __init__(self):
        InputSection.__init__(self)
        self.RI_INFO = _ri_info13()
        self.RI_DENSITY_COEFFS = _ri_density_coeffs13()
        self.RI_METRIC_2C_INTS = _ri_metric_2c_ints13()
        self._name = "PRINT"
        self._subsections = {'RI_INFO': 'RI_INFO', 'RI_DENSITY_COEFFS': 'RI_DENSITY_COEFFS', 'RI_METRIC_2C_INTS': 'RI_METRIC_2C_INTS'}


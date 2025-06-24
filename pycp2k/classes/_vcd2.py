from pycp2k.inputsection import InputSection
from ._print91 import _print91
from ._interpolator15 import _interpolator15


class _vcd2(InputSection):
    def __init__(self):
        InputSection.__init__(self)
        self.Section_parameters = None
        self.List_of_atoms = []
        self.Distributed_origin = None
        self.Origin_dependent_mfp = None
        self.Orbital_center = None
        self.Magnetic_origin = None
        self.Magnetic_origin_reference = None
        self.Spatial_origin = None
        self.Spatial_origin_reference = None
        self.PRINT = _print91()
        self.INTERPOLATOR = _interpolator15()
        self._name = "VCD"
        self._keywords = {'Distributed_origin': 'DISTRIBUTED_ORIGIN', 'Origin_dependent_mfp': 'ORIGIN_DEPENDENT_MFP', 'Orbital_center': 'ORBITAL_CENTER', 'Magnetic_origin': 'MAGNETIC_ORIGIN', 'Magnetic_origin_reference': 'MAGNETIC_ORIGIN_REFERENCE', 'Spatial_origin': 'SPATIAL_ORIGIN', 'Spatial_origin_reference': 'SPATIAL_ORIGIN_REFERENCE'}
        self._repeated_keywords = {'List_of_atoms': 'LIST_OF_ATOMS'}
        self._subsections = {'PRINT': 'PRINT', 'INTERPOLATOR': 'INTERPOLATOR'}
        self._aliases = {'Do_gauge': 'Distributed_origin'}
        self._attributes = ['Section_parameters']


    @property
    def Do_gauge(self):
        """
        See documentation for Distributed_origin
        """
        return self.Distributed_origin

    @Do_gauge.setter
    def Do_gauge(self, value):
        self.Distributed_origin = value

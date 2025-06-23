from pycp2k.inputsection import InputSection


class _harris_method1(InputSection):
    def __init__(self):
        InputSection.__init__(self)
        self.Section_parameters = None
        self.Energy_functional = None
        self.Density_source = None
        self.Orbital_basis = None
        self.Debug_forces = None
        self.Debug_stress = None
        self._name = "HARRIS_METHOD"
        self._keywords = {'Energy_functional': 'ENERGY_FUNCTIONAL', 'Density_source': 'DENSITY_SOURCE', 'Orbital_basis': 'ORBITAL_BASIS', 'Debug_forces': 'DEBUG_FORCES', 'Debug_stress': 'DEBUG_STRESS'}
        self._attributes = ['Section_parameters']


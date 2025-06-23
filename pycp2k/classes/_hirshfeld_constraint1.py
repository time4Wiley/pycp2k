from pycp2k.inputsection import InputSection


class _hirshfeld_constraint1(InputSection):
    def __init__(self):
        InputSection.__init__(self)
        self.Shape_function = None
        self.Gaussian_shape = None
        self.Gaussian_radius = None
        self.Atomic_radii = None
        self.Use_bohr = None
        self.Print_density = None
        self.Atoms_memory = None
        self.Use_atomic_cutoff = None
        self.Eps_cutoff = None
        self.Atomic_cutoff = None
        self._name = "HIRSHFELD_CONSTRAINT"
        self._keywords = {'Shape_function': 'SHAPE_FUNCTION', 'Gaussian_shape': 'GAUSSIAN_SHAPE', 'Gaussian_radius': 'GAUSSIAN_RADIUS', 'Atomic_radii': 'ATOMIC_RADII', 'Use_bohr': 'USE_BOHR', 'Print_density': 'PRINT_DENSITY', 'Atoms_memory': 'ATOMS_MEMORY', 'Use_atomic_cutoff': 'USE_ATOMIC_CUTOFF', 'Eps_cutoff': 'EPS_CUTOFF', 'Atomic_cutoff': 'ATOMIC_CUTOFF'}


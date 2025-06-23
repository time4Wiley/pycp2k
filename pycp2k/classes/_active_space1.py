from pycp2k.inputsection import InputSection
from ._fcidump1 import _fcidump1
from ._print_orbital_cubes1 import _print_orbital_cubes1
from ._eri1 import _eri1
from ._eri_gpw1 import _eri_gpw1
from ._localize3 import _localize3
from ._socket1 import _socket1


class _active_space1(InputSection):
    def __init__(self):
        InputSection.__init__(self)
        self.Section_parameters = None
        self.Model = None
        self.Active_electrons = None
        self.Active_orbitals = None
        self.Active_orbital_indices = None
        self.Isolated_system = None
        self.Orbital_selection = None
        self.Subspace_atom = None
        self.Subspace_shell = None
        self.Scf_embedding = None
        self.Qcschema = None
        self.As_solver = None
        self.Eps_iter = None
        self.Max_iter = None
        self.FCIDUMP = _fcidump1()
        self.PRINT_ORBITAL_CUBES = _print_orbital_cubes1()
        self.ERI = _eri1()
        self.ERI_GPW = _eri_gpw1()
        self.LOCALIZE = _localize3()
        self.SOCKET = _socket1()
        self._name = "ACTIVE_SPACE"
        self._keywords = {'Model': 'MODEL', 'Active_electrons': 'ACTIVE_ELECTRONS', 'Active_orbitals': 'ACTIVE_ORBITALS', 'Active_orbital_indices': 'ACTIVE_ORBITAL_INDICES', 'Isolated_system': 'ISOLATED_SYSTEM', 'Orbital_selection': 'ORBITAL_SELECTION', 'Subspace_atom': 'SUBSPACE_ATOM', 'Subspace_shell': 'SUBSPACE_SHELL', 'Scf_embedding': 'SCF_EMBEDDING', 'Qcschema': 'QCSCHEMA', 'As_solver': 'AS_SOLVER', 'Eps_iter': 'EPS_ITER', 'Max_iter': 'MAX_ITER'}
        self._subsections = {'FCIDUMP': 'FCIDUMP', 'PRINT_ORBITAL_CUBES': 'PRINT_ORBITAL_CUBES', 'ERI': 'ERI', 'ERI_GPW': 'ERI_GPW', 'LOCALIZE': 'LOCALIZE', 'SOCKET': 'SOCKET'}
        self._attributes = ['Section_parameters']


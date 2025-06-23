from pycp2k.inputsection import InputSection
from ._program_run_info3 import _program_run_info3


class _debug1(InputSection):
    def __init__(self):
        InputSection.__init__(self)
        self.Debug_forces = None
        self.Debug_stress_tensor = None
        self.Debug_dipole = None
        self.Debug_polarizability = None
        self.Dx = None
        self.De = None
        self.Max_relative_error = None
        self.Eps_no_error_check = None
        self.Stop_on_mismatch = None
        self.Check_dipole_dirs = None
        self.Check_atom_force = []
        self.PROGRAM_RUN_INFO = _program_run_info3()
        self._name = "DEBUG"
        self._keywords = {'Debug_forces': 'DEBUG_FORCES', 'Debug_stress_tensor': 'DEBUG_STRESS_TENSOR', 'Debug_dipole': 'DEBUG_DIPOLE', 'Debug_polarizability': 'DEBUG_POLARIZABILITY', 'Dx': 'DX', 'De': 'DE', 'Max_relative_error': 'MAX_RELATIVE_ERROR', 'Eps_no_error_check': 'EPS_NO_ERROR_CHECK', 'Stop_on_mismatch': 'STOP_ON_MISMATCH', 'Check_dipole_dirs': 'CHECK_DIPOLE_DIRS'}
        self._repeated_keywords = {'Check_atom_force': 'CHECK_ATOM_FORCE'}
        self._subsections = {'PROGRAM_RUN_INFO': 'PROGRAM_RUN_INFO'}


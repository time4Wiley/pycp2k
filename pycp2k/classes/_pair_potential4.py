from pycp2k.inputsection import InputSection
from ._print_dftd4 import _print_dftd4
from ._eeq5 import _eeq5


class _pair_potential4(InputSection):
    def __init__(self):
        InputSection.__init__(self)
        self.R_cutoff = None
        self.D4_cutoff = None
        self.D4_cn_cutoff = None
        self.Type = None
        self.Parameter_file_name = None
        self.Reference_functional = None
        self.D4_reference_code = None
        self.D4_debug = None
        self.D2_scaling = None
        self.D2_exp_pre = None
        self.Eps_cn = None
        self.D3_scaling = None
        self.D3bj_scaling = None
        self.D4_scaling = None
        self.Calculate_c9_term = None
        self.Reference_c9_term = None
        self.Factor_s9_term = None
        self.Long_range_correction = None
        self.Short_range_correction = None
        self.Short_range_correction_parameters = None
        self.Molecule_correction = None
        self.Molecule_correction_c8 = None
        self.Verbose_output = None
        self.D3_exclude_kind = None
        self.D3_exclude_kind_pair = []
        self.Kind_coordination_numbers = []
        self.Atom_coordination_numbers = []
        self.Atomparm = []
        self.PRINT_DFTD = _print_dftd4()
        self.EEQ = _eeq5()
        self._name = "PAIR_POTENTIAL"
        self._keywords = {'R_cutoff': 'R_CUTOFF', 'D4_cutoff': 'D4_CUTOFF', 'D4_cn_cutoff': 'D4_CN_CUTOFF', 'Type': 'TYPE', 'Parameter_file_name': 'PARAMETER_FILE_NAME', 'Reference_functional': 'REFERENCE_FUNCTIONAL', 'D4_reference_code': 'D4_REFERENCE_CODE', 'D4_debug': 'D4_DEBUG', 'D2_scaling': 'D2_SCALING', 'D2_exp_pre': 'D2_EXP_PRE', 'Eps_cn': 'EPS_CN', 'D3_scaling': 'D3_SCALING', 'D3bj_scaling': 'D3BJ_SCALING', 'D4_scaling': 'D4_SCALING', 'Calculate_c9_term': 'CALCULATE_C9_TERM', 'Reference_c9_term': 'REFERENCE_C9_TERM', 'Factor_s9_term': 'FACTOR_S9_TERM', 'Long_range_correction': 'LONG_RANGE_CORRECTION', 'Short_range_correction': 'SHORT_RANGE_CORRECTION', 'Short_range_correction_parameters': 'SHORT_RANGE_CORRECTION_PARAMETERS', 'Molecule_correction': 'MOLECULE_CORRECTION', 'Molecule_correction_c8': 'MOLECULE_CORRECTION_C8', 'Verbose_output': 'VERBOSE_OUTPUT', 'D3_exclude_kind': 'D3_EXCLUDE_KIND'}
        self._repeated_keywords = {'D3_exclude_kind_pair': 'D3_EXCLUDE_KIND_PAIR', 'Kind_coordination_numbers': 'KIND_COORDINATION_NUMBERS', 'Atom_coordination_numbers': 'ATOM_COORDINATION_NUMBERS', 'Atomparm': 'ATOMPARM'}
        self._subsections = {'PRINT_DFTD': 'PRINT_DFTD', 'EEQ': 'EEQ'}
        self._aliases = {'D3_cutoff': 'R_cutoff', 'D4_3b_cutoff': 'R_cutoff', 'Scaling': 'D2_scaling', 'Exp_pre': 'D2_exp_pre'}


    @property
    def D3_cutoff(self):
        """
        See documentation for R_cutoff
        """
        return self.R_cutoff

    @property
    def D4_3b_cutoff(self):
        """
        See documentation for R_cutoff
        """
        return self.R_cutoff

    @property
    def Scaling(self):
        """
        See documentation for D2_scaling
        """
        return self.D2_scaling

    @property
    def Exp_pre(self):
        """
        See documentation for D2_exp_pre
        """
        return self.D2_exp_pre

    @D3_cutoff.setter
    def D3_cutoff(self, value):
        self.R_cutoff = value

    @D4_3b_cutoff.setter
    def D4_3b_cutoff(self, value):
        self.R_cutoff = value

    @Scaling.setter
    def Scaling(self, value):
        self.D2_scaling = value

    @Exp_pre.setter
    def Exp_pre(self, value):
        self.D2_exp_pre = value

from pycp2k.inputsection import InputSection
from ._parameter2 import _parameter2
from ._nonbonded1 import _nonbonded1
from ._eeq3 import _eeq3


class _xtb1(InputSection):
    def __init__(self):
        InputSection.__init__(self)
        self.Gfn_type = None
        self.Do_ewald = None
        self.Sto_ng = None
        self.Hydrogen_sto_ng = None
        self.Use_halogen_correction = None
        self.Do_nonbonded = None
        self.Vdw_potential = None
        self.Coulomb_interaction = None
        self.Coulomb_lr = None
        self.Tb3_interaction = None
        self.Check_atomic_charges = None
        self.Eps_pairpotential = None
        self.En_shift_type = None
        self.PARAMETER = _parameter2()
        self.NONBONDED = _nonbonded1()
        self.EEQ = _eeq3()
        self._name = "XTB"
        self._keywords = {'Gfn_type': 'GFN_TYPE', 'Do_ewald': 'DO_EWALD', 'Sto_ng': 'STO_NG', 'Hydrogen_sto_ng': 'HYDROGEN_STO_NG', 'Use_halogen_correction': 'USE_HALOGEN_CORRECTION', 'Do_nonbonded': 'DO_NONBONDED', 'Vdw_potential': 'VDW_POTENTIAL', 'Coulomb_interaction': 'COULOMB_INTERACTION', 'Coulomb_lr': 'COULOMB_LR', 'Tb3_interaction': 'TB3_INTERACTION', 'Check_atomic_charges': 'CHECK_ATOMIC_CHARGES', 'Eps_pairpotential': 'EPS_PAIRPOTENTIAL', 'En_shift_type': 'EN_SHIFT_TYPE'}
        self._subsections = {'PARAMETER': 'PARAMETER', 'NONBONDED': 'NONBONDED', 'EEQ': 'EEQ'}


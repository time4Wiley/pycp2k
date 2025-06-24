#!/usr/bin/env python3
"""
PyCP2K script to create binding energy calculation inputs for:
1. PVA-OH + B(OH)3 complex
2. CBA-COO- + B(OH)4- complex

Compatible with CP2K 2023.1 - uses &MOTION/&GEO_OPT instead of &OPTIMIZATION
"""

from pycp2k import CP2K
import os


def create_basic_dft_setup(calc, project_name):
    """Configure basic DFT parameters for CP2K 2023.1"""
    calc.CP2K_INPUT.GLOBAL.Project_name = project_name
    calc.CP2K_INPUT.GLOBAL.Run_type = "ENERGY"
    calc.CP2K_INPUT.GLOBAL.Print_level = "MEDIUM"
    
    # Add FORCE_EVAL section
    calc.CP2K_INPUT.FORCE_EVAL_add()
    fe = calc.CP2K_INPUT.FORCE_EVAL_list[0]
    fe.Method = "Quickstep"
    
    # DFT setup
    fe.DFT.Basis_set_file_name = "BASIS_MOLOPT"
    fe.DFT.Potential_file_name = "GTH_POTENTIALS"
    fe.DFT.Charge = 0  # Will override for charged systems
    
    # XC functional - PBE
    fe.DFT.XC.XC_FUNCTIONAL.PBE.Scale_x = 1.0
    fe.DFT.XC.XC_FUNCTIONAL.PBE.Scale_c = 1.0
    
    # SCF parameters
    fe.DFT.SCF.Scf_guess = "ATOMIC"
    fe.DFT.SCF.Eps_scf = 1.0e-6
    fe.DFT.SCF.Max_scf = 50
    fe.DFT.SCF.MIXING.Method = "BROYDEN_MIXING"
    fe.DFT.SCF.MIXING.Alpha = 0.4
    fe.DFT.SCF.MIXING.Nbroyden = 8
    
    # MULTIGRID setup
    fe.DFT.MGRID.Cutoff = 400
    fe.DFT.MGRID.Rel_cutoff = 50
    fe.DFT.MGRID.Ngrids = 4
    
    # Cell - large box for gas phase
    fe.SUBSYS.CELL.A = "12.0 0.0 0.0"
    fe.SUBSYS.CELL.B = "0.0 12.0 0.0" 
    fe.SUBSYS.CELL.C = "0.0 0.0 12.0"
    fe.SUBSYS.CELL.Periodic = "NONE"
    
    return fe


def add_atoms_pva_borate(fe):
    """Add atoms for PVA-OH + B(OH)3 complex"""
    # For now, placeholder single oxygen atom
    # Will need real molecular coordinates later
    fe.SUBSYS.COORD.Default_keyword = """O  6.0  6.0  6.0"""
    
    # Kinds (atom types with basis sets and pseudopotentials)
    kind_o = fe.SUBSYS.KIND_add("O")
    kind_o.Basis_set = "DZVP-MOLOPT-SR-GTH"
    kind_o.Potential = "GTH-PBE-q6"


def add_atoms_cba_borate(fe):
    """Add atoms for CBA-COO- + B(OH)4- complex"""
    # For now, placeholder single oxygen atom
    # Will need real molecular coordinates later
    fe.SUBSYS.COORD.Default_keyword = """O  6.0  6.0  6.0"""
    
    # Charge = -2 for COO- + OH- (B(OH)4- is -1, COO- is -1)
    fe.DFT.Charge = -2
    
    # Kinds
    kind_o = fe.SUBSYS.KIND_add("O")
    kind_o.Basis_set = "DZVP-MOLOPT-SR-GTH"
    kind_o.Potential = "GTH-PBE-q6"


def create_inputs():
    """Create input files for both binding energy calculations"""
    
    # Create directories
    os.makedirs("energy_compare/01_pva_borate", exist_ok=True)
    os.makedirs("energy_compare/02_cba_borate", exist_ok=True)
    
    # PVA-borate calculation
    print("Creating PVA-borate input...")
    calc1 = CP2K()
    calc1.working_directory = "energy_compare/01_pva_borate"
    fe1 = create_basic_dft_setup(calc1, "pva_borate_energy")
    add_atoms_pva_borate(fe1)
    
    with open("energy_compare/01_pva_borate/bond_energy.inp", "w") as f:
        f.write(calc1.get_input_string())
    
    # CBA-borate calculation  
    print("Creating CBA-borate input...")
    calc2 = CP2K()
    calc2.working_directory = "energy_compare/02_cba_borate"
    fe2 = create_basic_dft_setup(calc2, "cba_borate_energy")
    add_atoms_cba_borate(fe2)
    
    with open("energy_compare/02_cba_borate/bond_energy.inp", "w") as f:
        f.write(calc2.get_input_string())
    
    print("✓ CP2K input files created!")
    print("  - energy_compare/01_pva_borate/bond_energy.inp")
    print("  - energy_compare/02_cba_borate/bond_energy.inp")
    print("\nNote: Using placeholder coordinates - update with real molecular structures")


if __name__ == "__main__":
    create_inputs() 
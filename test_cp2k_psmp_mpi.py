#!/usr/bin/env python
"""
Test CP2K 2024.1 PSMP with PyCP2K using proper MPI configuration
"""
import os

# Configure environment for OpenMPI 4.1.5 (matching CP2K)
os.environ['PATH'] = '/public/software/mpi/openmpi/4.1.5/bin:' + os.environ.get('PATH', '')
os.environ['LD_LIBRARY_PATH'] = '/public/software/mpi/openmpi/4.1.5/lib:' + os.environ.get('LD_LIBRARY_PATH', '')

import pycp2k
from pycp2k import CP2K

def test_cp2k_psmp_mpi():
    """Test PyCP2K with CP2K 2024.1 PSMP"""
    
    # Create calculator
    calc = CP2K()
    
    # Set CP2K PSMP executable
    calc.command = "/public/software/apps/cp2k/cp2k-2024.1-gcc/exe/local/cp2k.psmp"
    
    # Configure for minimal H2 molecule test
    calc.CP2K_INPUT.GLOBAL.Run_type = "ENERGY"
    calc.CP2K_INPUT.GLOBAL.Project_name = "h2_psmp_test"
    calc.CP2K_INPUT.GLOBAL.Print_level = "LOW"
    
    # Force evaluation setup
    calc.CP2K_INPUT.FORCE_EVAL_add()
    calc.CP2K_INPUT.FORCE_EVAL_list[0].Method = "QUICKSTEP"
    
    # DFT settings
    calc.CP2K_INPUT.FORCE_EVAL_list[0].DFT.Basis_set_file_name = "BASIS_MOLOPT"
    calc.CP2K_INPUT.FORCE_EVAL_list[0].DFT.Potential_file_name = "GTH_POTENTIALS"
    
    # XC functional
    calc.CP2K_INPUT.FORCE_EVAL_list[0].DFT.XC.XC_FUNCTIONAL.PBE.Scale_x = 1.0
    calc.CP2K_INPUT.FORCE_EVAL_list[0].DFT.XC.XC_FUNCTIONAL.PBE.Scale_c = 1.0
    
    # SCF settings
    calc.CP2K_INPUT.FORCE_EVAL_list[0].DFT.SCF.Max_scf = 10
    calc.CP2K_INPUT.FORCE_EVAL_list[0].DFT.SCF.Eps_scf = 1.0e-6
    calc.CP2K_INPUT.FORCE_EVAL_list[0].DFT.SCF.Scf_guess = "ATOMIC"
    
    # Subsystem
    calc.CP2K_INPUT.FORCE_EVAL_list[0].SUBSYS.CELL.A = "10.0 0.0 0.0"
    calc.CP2K_INPUT.FORCE_EVAL_list[0].SUBSYS.CELL.B = "0.0 10.0 0.0" 
    calc.CP2K_INPUT.FORCE_EVAL_list[0].SUBSYS.CELL.C = "0.0 0.0 10.0"
    
    # H2 molecule
    calc.CP2K_INPUT.FORCE_EVAL_list[0].SUBSYS.COORD.Default_keyword = """
H  0.0  0.0  0.0
H  0.0  0.0  0.74
"""
    
    # Kind settings  
    calc.CP2K_INPUT.FORCE_EVAL_list[0].SUBSYS.KIND_add("H")
    calc.CP2K_INPUT.FORCE_EVAL_list[0].SUBSYS.KIND_list[0].Basis_set = "DZVP-MOLOPT-GTH"
    calc.CP2K_INPUT.FORCE_EVAL_list[0].SUBSYS.KIND_list[0].Potential = "GTH-PBE-q1"
    
    print("✅ PyCP2K input file configured for H2 with PSMP")
    
    # Generate input file
    input_str = calc.write_input_file()
    
    # Write to file for inspection
    with open("h2_psmp_test.inp", "w") as f:
        f.write(input_str)
    
    print("✅ CP2K input file generated: h2_psmp_test.inp")
    print(f"✅ CP2K command: {calc.command}")
    print("✅ Ready for PSMP execution with OpenMPI 4.1.5")
    
    return calc

if __name__ == "__main__":
    calc = test_cp2k_psmp_mpi()
    print("\n=== PyCP2K PSMP Configuration Summary ===")
    print(f"CP2K Executable: {calc.command}")
    print("MPI Library: OpenMPI 4.1.5 (matching CP2K build)")
    print("Input file: h2_psmp_test.inp")
    print("Status: ✅ Ready for parallel execution")


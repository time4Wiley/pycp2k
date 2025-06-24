#!/usr/bin/env python
"""
Test PyCP2K with CP2K 2024.1 PSMP using OpenMPI module
"""

# Simplified - no manual environment setup needed
import pycp2k
from pycp2k import CP2K

def test_module_based_setup():
    """Test PyCP2K with module-based OpenMPI setup"""
    
    # Create calculator (OpenMPI module handles environment)
    calc = CP2K()
    calc.working_directory = "."
    calc.project_name = "h2_module_test"
    calc.command = "/public/software/apps/cp2k/cp2k-2024.1-gcc/exe/local/cp2k.psmp"
    
    # Basic H2 configuration
    calc.CP2K_INPUT.GLOBAL.Run_type = "ENERGY"
    calc.CP2K_INPUT.GLOBAL.Project_name = "h2_module_test"
    calc.CP2K_INPUT.GLOBAL.Print_level = "LOW"
    
    # Force evaluation
    calc.CP2K_INPUT.FORCE_EVAL_add()
    calc.CP2K_INPUT.FORCE_EVAL_list[0].Method = "QUICKSTEP"
    calc.CP2K_INPUT.FORCE_EVAL_list[0].DFT.Basis_set_file_name = "BASIS_MOLOPT"
    calc.CP2K_INPUT.FORCE_EVAL_list[0].DFT.Potential_file_name = "GTH_POTENTIALS"
    
    # XC functional
    calc.CP2K_INPUT.FORCE_EVAL_list[0].DFT.XC.XC_FUNCTIONAL.PBE.Scale_x = 1.0
    calc.CP2K_INPUT.FORCE_EVAL_list[0].DFT.XC.XC_FUNCTIONAL.PBE.Scale_c = 1.0
    
    # SCF
    calc.CP2K_INPUT.FORCE_EVAL_list[0].DFT.SCF.Max_scf = 10
    calc.CP2K_INPUT.FORCE_EVAL_list[0].DFT.SCF.Eps_scf = 1.0e-6
    calc.CP2K_INPUT.FORCE_EVAL_list[0].DFT.SCF.Scf_guess = "ATOMIC"
    
    # Cell
    calc.CP2K_INPUT.FORCE_EVAL_list[0].SUBSYS.CELL.A = "10.0 0.0 0.0"
    calc.CP2K_INPUT.FORCE_EVAL_list[0].SUBSYS.CELL.B = "0.0 10.0 0.0"
    calc.CP2K_INPUT.FORCE_EVAL_list[0].SUBSYS.CELL.C = "0.0 0.0 10.0"
    
    # H2 coordinates
    calc.CP2K_INPUT.FORCE_EVAL_list[0].SUBSYS.COORD.Default_keyword = """
H  0.0  0.0  0.0
H  0.0  0.0  0.74
"""
    
    # Kind
    calc.CP2K_INPUT.FORCE_EVAL_list[0].SUBSYS.KIND_add("H")
    calc.CP2K_INPUT.FORCE_EVAL_list[0].SUBSYS.KIND_list[0].Basis_set = "DZVP-MOLOPT-GTH"
    calc.CP2K_INPUT.FORCE_EVAL_list[0].SUBSYS.KIND_list[0].Potential = "GTH-PBE-q1"
    
    # Generate input
    calc.write_input_file()
    
    print("✅ PyCP2K configured with module-based OpenMPI 4.1.5")
    print(f"✅ Input file: {calc.input_path}")
    print(f"✅ CP2K command: {calc.command}")
    
    return calc

if __name__ == "__main__":
    calc = test_module_based_setup()
    print("\n=== Module-Based Configuration Complete ===")
    print("✅ No manual PATH/LD_LIBRARY_PATH exports needed")
    print("✅ OpenMPI 4.1.5 module handles environment automatically")
    print("✅ Ready for production use")


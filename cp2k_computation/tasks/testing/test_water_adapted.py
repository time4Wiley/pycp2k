#!/usr/bin/env python3
"""
test_water_simple.py
Simplest possible test - just water molecule
"""

import sys
import time
import subprocess
from pathlib import Path
sys.path.insert(0, '..')
from pycp2k import CP2K

def create_water_test():
    """Create simple water molecule test"""
    
    calc = CP2K()
    calc.working_directory = "./"
    calc.project_name = "water_test"
    
    # Main sections
    CP2K_INPUT = calc.CP2K_INPUT
    GLOBAL = CP2K_INPUT.GLOBAL
    FORCE_EVAL = CP2K_INPUT.FORCE_EVAL_add()
    
    # Global settings
    GLOBAL.Project_name = "water_test"
    GLOBAL.Run_type = "ENERGY"
    GLOBAL.Print_level = "LOW"
    
    # Force evaluation
    FORCE_EVAL.Method = "Quickstep"
    
    # DFT settings
    dft = FORCE_EVAL.DFT
    dft.Basis_set_file_name = "BASIS_MOLOPT"
    dft.Potential_file_name = "GTH_POTENTIALS"
    
    # Very conservative settings
    dft.MGRID.Cutoff = 150
    dft.MGRID.Rel_cutoff = 20
    
    # SCF settings
    dft.SCF.Eps_scf = 1.0e-4
    dft.SCF.Max_scf = 20
    dft.SCF.OT.Preconditioner = "FULL_SINGLE_INVERSE"
    dft.SCF.OT.Minimizer = "DIIS"
    
    # Simple functional
    dft.XC.XC_FUNCTIONAL.Section_parameters = "PBE"
    
    # Small cell
    cell = FORCE_EVAL.SUBSYS.CELL
    cell.A = [8.0, 0, 0]
    cell.B = [0, 8.0, 0] 
    cell.C = [0, 0, 8.0]
    cell.Periodic = "NONE"
    
    # Water molecule coordinates
    coords = [
        ["O",  0.0,  0.0,  0.0],
        ["H",  0.8,  0.6,  0.0],
        ["H", -0.8,  0.6,  0.0],
    ]
    
    # Add coordinates
    for symbol, x, y, z in coords:
        FORCE_EVAL.SUBSYS.COORD.Default_keyword.append([symbol, x, y, z])
    
    # Only H and O kinds - no problematic elements
    kind_o = FORCE_EVAL.SUBSYS.KIND_add("O")
    kind_o.Basis_set = "SZV-MOLOPT-GTH"
    kind_o.Potential = "GTH-PBE-q6"
    
    kind_h = FORCE_EVAL.SUBSYS.KIND_add("H")
    kind_h.Basis_set = "SZV-MOLOPT-GTH"
    kind_h.Potential = "GTH-PBE-q1"
    
    return calc

def run_water_test():
    """Run water test"""
    
    print("💧 Simple Water Test for M1 MacBook")
    print("=" * 40)
    
    # Create input
    calc = create_water_test()
    input_file = "water_test.inp"
    calc.write_input_file(input_file)
    print(f"✅ Created {input_file} (3 atoms: H₂O)")
    
    # Run test
    print(f"\n⏱️  Running CP2K...")
    start_time = time.time()
    
    try:
        cmd = ['mpirun -np 1 cp2k.psmp', '-i', input_file, '-o', 'water_test.out']
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        
        end_time = time.time()
        runtime = end_time - start_time
        
        if result.returncode == 0:
            print(f"✅ Success! Runtime: {runtime:.2f} seconds")
            
            # Parse energy
            if Path('water_test.out').exists():
                with open('water_test.out', 'r') as f:
                    output = f.read()
                for line in output.split('\n'):
                    if 'Total FORCE_EVAL' in line and 'energy' in line:
                        print(f"🔬 {line.strip()}")
                        break
            
            return True, runtime
        else:
            print(f"❌ Failed:")
            print("STDOUT:", result.stdout[-300:] if result.stdout else "None")
            print("STDERR:", result.stderr[-300:] if result.stderr else "None")
            return False, 0
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False, 0

def cleanup():
    """Clean up"""
    files = ['water_test.inp', 'water_test.out', 'water_test-RESTART.wfn']
    for f in files:
        if Path(f).exists():
            Path(f).unlink()

if __name__ == "__main__":
    success, runtime = run_water_test()
    
    if success:
        print("\n🎉 Water test successful!")
        print(f"   Runtime: {runtime:.2f}s for 3-atom system")
        print("   Your M1 Pro can run CP2K calculations!")
        
        # Quick estimate
        print(f"\n📊 Quick estimates for ultra-minimal systems:")
        for atoms in [3, 5, 7, 9]:
            est_time = runtime * ((atoms/3)**2.5)
            print(f"   {atoms} atoms: ~{est_time:.1f}s per SCF step")
        
    else:
        print("\n❌ Even water test failed - CP2K installation issue")
    
    cleanup()
    print("\n🧹 Cleaned up") 
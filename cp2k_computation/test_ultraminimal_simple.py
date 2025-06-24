#!/usr/bin/env python3
"""
test_ultraminimal_simple.py
Simple ultra-minimal test for M1 MacBook performance verification
"""

import sys
import time
import subprocess
from pathlib import Path
sys.path.insert(0, '..')
from pycp2k import CP2K

def create_simple_boronate_test():
    """Create simple 5-atom boronate test: B(OH)3"""
    
    calc = CP2K()
    calc.working_directory = "./"
    calc.project_name = "ultramin_test"
    
    # Main sections
    CP2K_INPUT = calc.CP2K_INPUT
    GLOBAL = CP2K_INPUT.GLOBAL
    FORCE_EVAL = CP2K_INPUT.FORCE_EVAL_add()
    
    # Global settings
    GLOBAL.Project_name = "ultramin_test"
    GLOBAL.Run_type = "ENERGY"
    GLOBAL.Print_level = "LOW"
    
    # Force evaluation
    FORCE_EVAL.Method = "Quickstep"
    
    # Fast DFT settings
    dft = FORCE_EVAL.DFT
    dft.Basis_set_file_name = "BASIS_MOLOPT"
    dft.Potential_file_name = "GTH_POTENTIALS"
    
    # Aggressive speed settings
    dft.MGRID.Cutoff = 150     # Very low for speed
    dft.MGRID.Rel_cutoff = 20
    
    # SCF settings
    dft.SCF.Eps_scf = 1.0e-4   # Relaxed convergence
    dft.SCF.Max_scf = 15
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
    
    # B(OH)3 coordinates - 7 atoms
    coords = [
        ["B",  0.0,  0.0,  0.0],
        ["O", -0.5,  1.2,  0.0],
        ["O",  1.0, -0.6,  0.0],
        ["O", -0.5, -0.6,  1.0],
        ["H", -1.4,  1.3,  0.0],
        ["H",  1.9, -0.7,  0.0],
        ["H", -1.4, -0.7,  1.0],
    ]
    
    # Add coordinates
    for symbol, x, y, z in coords:
        FORCE_EVAL.SUBSYS.COORD.Default_keyword.append([symbol, x, y, z])
    
    # Kinds
    kind_b = FORCE_EVAL.SUBSYS.KIND_add("B")
    kind_b.Basis_set = "SZV-MOLOPT-GTH"
    kind_b.Potential = "GTH-PBE-q3"
    
    kind_o = FORCE_EVAL.SUBSYS.KIND_add("O")
    kind_o.Basis_set = "SZV-MOLOPT-GTH"
    kind_o.Potential = "GTH-PBE-q6"
    
    kind_h = FORCE_EVAL.SUBSYS.KIND_add("H")
    kind_h.Basis_set = "SZV-MOLOPT-GTH"
    kind_h.Potential = "GTH-PBE-q1"
    
    return calc

def run_ultraminimal_test():
    """Run ultra-minimal test and time it"""
    
    print("🚀 Ultra-Minimal CP2K Test for M1 MacBook")
    print("=" * 50)
    
    # Create input
    calc = create_simple_boronate_test()
    input_file = "ultramin_test.inp"
    calc.write_input_file(input_file)
    print(f"✅ Created {input_file} (7 atoms: B(OH)₃)")
    
    # Run CP2K
    print("\n⏱️  Running CP2K...")
    start_time = time.time()
    
    try:
        cmd = ['cp2k.ssmp', '-i', input_file, '-o', 'ultramin_test.out']
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        
        end_time = time.time()
        runtime = end_time - start_time
        
        if result.returncode == 0:
            print(f"✅ Success! Runtime: {runtime:.2f} seconds")
            
            # Parse energy
            if Path('ultramin_test.out').exists():
                with open('ultramin_test.out', 'r') as f:
                    output = f.read()
                for line in output.split('\n'):
                    if 'Total FORCE_EVAL' in line and 'energy' in line:
                        print(f"🔬 {line.strip()}")
                        break
            
            return True, runtime
        else:
            print(f"❌ Failed: {result.stderr}")
            return False, 0
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False, 0

def estimate_performance(test_runtime):
    """Estimate performance for different systems"""
    
    print(f"\n📊 M1 MacBook Performance Estimates")
    print("=" * 50)
    
    # Scaling from 7-atom test
    systems = [
        ("B(OH)₃ Test", 7, test_runtime),
        ("Ultra Ti₃C₂", 5, 0),
        ("Ultra Combined", 8, 0),
        ("Ultra Boronate-Diol", 9, 0),
    ]
    
    print(f"{'System':<25} {'Atoms':<6} {'SCF':<8} {'Geo Opt':<10}")
    print("-" * 55)
    
    total_est = 0
    scaling = 2.5  # Conservative estimate
    
    for name, atoms, runtime in systems:
        if atoms == 7:  # Reference
            scf_time = runtime
            geo_time = runtime
        else:
            scale = (atoms / 7) ** scaling
            scf_time = test_runtime * scale
            geo_time = scf_time * 25  # ~25 geo steps
            total_est += geo_time
        
        print(f"{name:<25} {atoms:<6} {scf_time:.1f}s    {geo_time/60:.1f}min")
    
    print(f"\n💡 Summary:")
    print(f"   • Total suite time: ~{total_est/60:.0f} minutes")
    print(f"   • Rating: {'Excellent' if total_est < 1800 else 'Good' if total_est < 3600 else 'Moderate'}")
    
    return total_est

def cleanup_files():
    """Clean up test files"""
    files = ['ultramin_test.inp', 'ultramin_test.out', 'ultramin_test-RESTART.wfn']
    for f in files:
        if Path(f).exists():
            Path(f).unlink()

if __name__ == "__main__":
    success, runtime = run_ultraminimal_test()
    
    if success:
        estimate_performance(runtime)
        cleanup_files()
        print("\n🧹 Files cleaned up")
    else:
        print("\n❌ Test failed") 
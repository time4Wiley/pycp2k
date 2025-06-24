#!/usr/bin/env python3
"""
test_m1_final.py
Final corrected ultra-minimal test for M1 MacBook performance verification
Uses correct basis sets and serial CP2K
"""

import sys
import time
import subprocess
from pathlib import Path
sys.path.insert(0, '..')
from pycp2k import CP2K

def create_corrected_boronate_test():
    """Create corrected 7-atom boronate test: B(OH)3"""
    
    calc = CP2K()
    calc.working_directory = "./"
    calc.project_name = "m1_test"
    
    # Main sections
    CP2K_INPUT = calc.CP2K_INPUT
    GLOBAL = CP2K_INPUT.GLOBAL
    FORCE_EVAL = CP2K_INPUT.FORCE_EVAL_add()
    
    # Global settings
    GLOBAL.Project_name = "m1_test"
    GLOBAL.Run_type = "ENERGY"
    GLOBAL.Print_level = "LOW"
    
    # Force evaluation
    FORCE_EVAL.Method = "Quickstep"
    
    # DFT settings optimized for M1
    dft = FORCE_EVAL.DFT
    dft.Basis_set_file_name = "BASIS_MOLOPT"
    dft.Potential_file_name = "GTH_POTENTIALS"
    
    # Conservative settings for stability
    dft.MGRID.Cutoff = 200     # Reasonable for testing
    dft.MGRID.Rel_cutoff = 30
    
    # SCF settings
    dft.SCF.Eps_scf = 1.0e-5   # Good convergence
    dft.SCF.Max_scf = 30
    dft.SCF.OT.Preconditioner = "FULL_SINGLE_INVERSE"
    dft.SCF.OT.Minimizer = "DIIS"
    
    # Simple functional
    dft.XC.XC_FUNCTIONAL.Section_parameters = "PBE"
    
    # Reasonable cell
    cell = FORCE_EVAL.SUBSYS.CELL
    cell.A = [10.0, 0, 0]
    cell.B = [0, 10.0, 0] 
    cell.C = [0, 0, 10.0]
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
    
    # Correct basis sets for each element
    kind_b = FORCE_EVAL.SUBSYS.KIND_add("B")
    kind_b.Basis_set = "SZV-MOLOPT-SR-GTH"  # Use SR version for boron
    kind_b.Potential = "GTH-PBE-q3"
    
    kind_o = FORCE_EVAL.SUBSYS.KIND_add("O")
    kind_o.Basis_set = "SZV-MOLOPT-GTH"     # Regular for oxygen
    kind_o.Potential = "GTH-PBE-q6"
    
    kind_h = FORCE_EVAL.SUBSYS.KIND_add("H")
    kind_h.Basis_set = "SZV-MOLOPT-GTH"     # Regular for hydrogen
    kind_h.Potential = "GTH-PBE-q1"
    
    return calc

def run_m1_performance_test():
    """Run performance test on M1 MacBook"""
    
    print("🚀 M1 Pro MacBook CP2K Performance Test")
    print("=" * 50)
    
    # Create input
    calc = create_corrected_boronate_test()
    input_file = "m1_test.inp"
    calc.write_input_file(input_file)
    print(f"✅ Created {input_file} (7 atoms: B(OH)₃)")
    
    # Test with correct executable
    print(f"\n⏱️  Running CP2K with cp2k.ssmp (serial SMP)...")
    start_time = time.time()
    
    try:
        cmd = ['cp2k.ssmp', '-i', input_file, '-o', 'm1_test.out']
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        
        end_time = time.time()
        runtime = end_time - start_time
        
        if result.returncode == 0:
            print(f"✅ Success! Runtime: {runtime:.2f} seconds")
            
            # Parse energy
            if Path('m1_test.out').exists():
                with open('m1_test.out', 'r') as f:
                    output = f.read()
                for line in output.split('\n'):
                    if 'Total FORCE_EVAL' in line and 'energy' in line:
                        print(f"🔬 {line.strip()}")
                        break
            
            return True, runtime
        else:
            print(f"❌ CP2K failed:")
            print(result.stderr[:500])  # First 500 chars of error
            return False, 0
            
    except subprocess.TimeoutExpired:
        print(f"❌ Timed out after 120 seconds")
        return False, 0
    except Exception as e:
        print(f"❌ Error: {e}")
        return False, 0

def estimate_realistic_performance(test_runtime):
    """Estimate realistic performance for ultra-minimal systems"""
    
    print(f"\n📊 Realistic M1 Pro Performance Estimates")
    print("=" * 60)
    
    # Scale from 7-atom test
    print("Based on working 7-atom B(OH)₃ test:")
    print()
    
    # Ultra-minimal systems with correct basis sets
    systems = [
        ("B(OH)₃ Reference", 7, test_runtime, "Tested"),
        ("Ultra H₂O", 3, 0, "Simple test"),
        ("Ultra BH₃", 4, 0, "Boron test"),
        ("Ultra C₂H₄", 6, 0, "Organic test"),
        ("Ultra B(OH)₂-H₂O", 8, 0, "Boronate complex"),
    ]
    
    print(f"{'System':<25} {'Atoms':<6} {'SCF Time':<10} {'Geo Opt':<10} {'Status':<15}")
    print("-" * 80)
    
    total_time = 0
    scaling = 2.4  # More conservative scaling
    
    for name, atoms, runtime, status in systems:
        if atoms == 7:  # Reference
            scf_time = runtime
            geo_time = runtime  # Single point
        else:
            scale = (atoms / 7) ** scaling
            scf_time = test_runtime * scale
            geo_time = scf_time * 20  # ~20 geo steps
            total_time += geo_time
        
        print(f"{name:<25} {atoms:<6} {scf_time:.1f}s      {geo_time/60:.1f}min     {status:<15}")
    
    print(f"\n💡 Realistic M1 Pro Estimates:")
    print(f"   • Ultra-minimal systems: {total_time/60:.0f} minutes total")
    print(f"   • Individual tests: 1-5 minutes each")
    print(f"   • Rating: {'Excellent' if total_time < 900 else 'Good' if total_time < 1800 else 'Moderate'}")
    
    # Recommendations
    print(f"\n🎯 Recommendations for M1 Pro:")
    if total_time < 900:
        print("   • Run all ultra-minimal tests locally")
        print("   • Perfect for method validation")
        print("   • Fast iteration cycles")
    elif total_time < 1800:
        print("   • Select most important tests for local runs")
        print("   • Good for development and debugging")
    else:
        print("   • Use only smallest systems locally")
        print("   • Consider cloud computing for larger tests")
    
    return total_time

def cleanup_files():
    """Clean up test files"""
    files = ['m1_test.inp', 'm1_test.out', 'm1_test-RESTART.wfn']
    for f in files:
        if Path(f).exists():
            Path(f).unlink()

if __name__ == "__main__":
    success, runtime = run_m1_performance_test()
    
    if success:
        estimate_realistic_performance(runtime)
        cleanup_files()
        print("\n🧹 Files cleaned up")
        print("\n🎉 M1 Pro CP2K verification complete!")
    else:
        print("\n❌ Test failed - debugging needed") 
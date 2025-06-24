#!/usr/bin/env python3
"""
test_local_cp2k.py
Simple H2 molecule test to verify local CP2K 2025.1 installation works with pycp2k.
Tests both input generation and actual CP2K execution on M1 Pro MacBook.
"""

import sys
import time
import subprocess
from pathlib import Path
sys.path.insert(0, '..')
from pycp2k import CP2K
from ase import Atoms

def create_h2_molecule():
    """Create simple H2 molecule"""
    # H2 molecule with bond length ~0.74 Angstrom
    positions = [
        [0.0, 0.0, 0.0],
        [0.74, 0.0, 0.0]
    ]
    symbols = ['H', 'H']
    atoms = Atoms(symbols=symbols, positions=positions)
    return atoms

def create_h2_cp2k_input():
    """Create minimal CP2K input for H2 energy calculation"""
    
    calc = CP2K()
    calc.working_directory = "./"
    calc.project_name = "h2_test"
    
    # Get main sections
    CP2K_INPUT = calc.CP2K_INPUT
    GLOBAL = CP2K_INPUT.GLOBAL
    FORCE_EVAL = CP2K_INPUT.FORCE_EVAL_add()
    
    # Global settings
    GLOBAL.Project_name = "h2_test"
    GLOBAL.Run_type = "ENERGY"
    GLOBAL.Print_level = "MEDIUM"
    
    # Force evaluation
    FORCE_EVAL.Method = "Quickstep"
    
    # DFT settings - minimal for speed
    dft = FORCE_EVAL.DFT
    dft.Basis_set_file_name = "BASIS_MOLOPT"
    dft.Potential_file_name = "GTH_POTENTIALS"
    
    # Small grid for fast testing
    dft.MGRID.Cutoff = 200  # Low cutoff for speed
    dft.MGRID.Rel_cutoff = 30
    
    # SCF settings
    dft.SCF.Eps_scf = 1.0e-5  # Relaxed for speed
    dft.SCF.Max_scf = 30
    dft.SCF.OT.Preconditioner = "FULL_SINGLE_INVERSE"
    dft.SCF.OT.Minimizer = "DIIS"
    
    # XC functional - simple PBE
    dft.XC.XC_FUNCTIONAL.Section_parameters = "PBE"
    
    # Small cell for isolated molecule
    cell = FORCE_EVAL.SUBSYS.CELL
    cell_size = 8.0
    cell.A = [cell_size, 0, 0]
    cell.B = [0, cell_size, 0]
    cell.C = [0, 0, cell_size]
    cell.Periodic = "NONE"  # Isolated molecule
    
    # Add H2 coordinates
    h2 = create_h2_molecule()
    for symbol, pos in zip(h2.get_chemical_symbols(), h2.get_positions()):
        FORCE_EVAL.SUBSYS.COORD.Default_keyword.append([symbol, pos[0], pos[1], pos[2]])
    
    # Hydrogen basis set and potential
    kind = FORCE_EVAL.SUBSYS.KIND_add("H")
    kind.Basis_set = "DZVP-MOLOPT-GTH"
    kind.Potential = "GTH-PBE-q1"
    
    return calc

def check_cp2k_executable():
    """Check if CP2K executable is available"""
    executables = ['cp2k.ssmp', 'cp2k.psmp', 'cp2k.sopt', 'cp2k']
    
    for exe in executables:
        try:
            result = subprocess.run([exe, '--version'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                print(f"✅ Found CP2K executable: {exe}")
                print(f"   Version info: {result.stdout.split('CP2K')[1].split()[0] if 'CP2K' in result.stdout else 'Unknown'}")
                return exe
        except (subprocess.TimeoutExpired, FileNotFoundError):
            continue
    
    print("❌ No CP2K executable found. Please check installation.")
    print("   Expected: cp2k.psmp, cp2k.sopt, or cp2k")
    return None

def run_h2_test():
    """Run complete H2 test"""
    
    print("🧪 Testing Local CP2K 2025.1 Installation")
    print("=" * 50)
    
    # 1. Check executable
    cp2k_exe = check_cp2k_executable()
    if not cp2k_exe:
        return False
    
    # 2. Create input
    print("\n📝 Creating H2 test input...")
    calc = create_h2_cp2k_input()
    
    # 3. Write input file
    input_file = "h2_test.inp"
    calc.write_input_file(input_file)
    print(f"   ✅ Written: {input_file}")
    
    # 4. Check input syntax
    if Path(input_file).exists():
        with open(input_file, 'r') as f:
            content = f.read()
        if '&GLOBAL' in content and '&FORCE_EVAL' in content:
            print("   ✅ Input syntax looks correct")
        else:
            print("   ❌ Input syntax issue")
            return False
    
    # 5. Run CP2K
    print(f"\n🚀 Running CP2K with {cp2k_exe}...")
    start_time = time.time()
    
    try:
        # Run CP2K as subprocess
        cmd = [cp2k_exe, '-i', input_file, '-o', 'h2_test.out']
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        
        end_time = time.time()
        runtime = end_time - start_time
        
        # Check results
        if result.returncode == 0:
            print(f"   ✅ CP2K completed successfully!")
            print(f"   ⏱️  Runtime: {runtime:.2f} seconds")
            
            # Parse energy if available
            if Path('h2_test.out').exists():
                with open('h2_test.out', 'r') as f:
                    output = f.read()
                
                # Look for total energy
                if 'Total FORCE_EVAL' in output:
                    for line in output.split('\n'):
                        if 'Total FORCE_EVAL' in line and 'energy' in line:
                            energy_line = line.strip()
                            print(f"   🔬 {energy_line}")
                            break
                
                print("   ✅ H2 calculation completed successfully!")
                return True, runtime
            
        else:
            print(f"   ❌ CP2K failed with return code: {result.returncode}")
            print(f"   Error: {result.stderr}")
            return False, 0
            
    except subprocess.TimeoutExpired:
        print("   ❌ CP2K timed out (>120s)")
        return False, 0
    except Exception as e:
        print(f"   ❌ Error running CP2K: {e}")
        return False, 0

def estimate_minimal_system_performance(h2_runtime):
    """Estimate performance for minimal systems based on H2 test"""
    
    print("\n📊 Performance Estimation for M1 Pro MacBook")
    print("=" * 50)
    
    # H2 has 2 atoms, minimal systems have 11-18 atoms
    # DFT scales roughly as O(N^2.7) for small systems
    scaling_factor = 2.7
    
    systems = [
        ("H2 Test", 2, h2_runtime),
        ("Minimal Ti3C2 Surface", 11, 0),
        ("Minimal Boronate-Diol", 15, 0),
        ("Minimal Combined", 18, 0)
    ]
    
    print(f"{'System':<25} {'Atoms':<6} {'Est. Time':<12} {'Total Est.':<12}")
    print("-" * 60)
    
    for name, atoms, runtime in systems:
        if atoms == 2:  # H2 reference
            total_est = f"{runtime:.1f}s"
            est_time = f"{runtime:.1f}s"
        else:
            # Estimate single-point energy time
            scale = (atoms / 2) ** scaling_factor
            single_point = h2_runtime * scale
            
            # Estimate total time for geometry optimization (typically 20-50 steps)
            geo_opt_steps = 30
            geo_opt_time = single_point * geo_opt_steps
            
            # Estimate MD time (1500 total steps for equilibration + production)
            md_steps = 1500
            md_time = single_point * md_steps
            
            est_time = f"{single_point:.1f}s/step"
            total_est = f"{(geo_opt_time + md_time)/60:.1f} min"
        
        print(f"{name:<25} {atoms:<6} {est_time:<12} {total_est:<12}")
    
    # Summary
    print("\n💡 Summary for M1 Pro MacBook:")
    base_time = h2_runtime * ((15/2)**scaling_factor)  # Average system size
    total_suite_time = base_time * (30 + 1500) * 3 / 60  # 3 systems
    
    print(f"   • Single SCF step: ~{base_time:.1f}s (15-atom average)")
    print(f"   • Complete test suite: ~{total_suite_time:.0f} minutes")
    print(f"   • Performance rating: {'Excellent' if total_suite_time < 60 else 'Good' if total_suite_time < 180 else 'Moderate'}")
    
    return total_suite_time

if __name__ == "__main__":
    success, runtime = run_h2_test()
    
    if success:
        print("\n🎉 Local CP2K installation verified!")
        estimate_minimal_system_performance(runtime)
        
        # Clean up test files
        test_files = ['h2_test.inp', 'h2_test.out', 'h2_test-RESTART.wfn']
        for f in test_files:
            if Path(f).exists():
                Path(f).unlink()
        print("\n🧹 Test files cleaned up")
        
    else:
        print("\n❌ Local CP2K installation test failed!")
        print("   Please check your CP2K installation and try again.") 
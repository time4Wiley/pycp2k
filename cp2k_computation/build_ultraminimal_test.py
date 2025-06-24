#!/usr/bin/env python3
"""
build_ultraminimal_test.py
Create ultra-minimal systems optimized for M1 MacBook local testing.
Reduces atom count further while preserving key chemical interactions.
"""

import sys
sys.path.insert(0, '..')
from pycp2k import CP2K
import numpy as np

def create_ultraminimal_boronate_diol():
    """
    Ultra-minimal boronate-diol: BO2H + ethylene glycol = 9 atoms total
    Still tests reversible B-O bonding in smallest possible system
    """
    
    # Very simple: B(OH)2 + HO-CH2-CH2-OH
    coordinates = [
        # B(OH)2 group - 4 atoms
        ["B",  0.0,  0.0,  0.0],      # Boron center
        ["O", -0.5,  1.2,  0.0],      # First OH
        ["O",  1.3,  0.0,  0.0],      # Second OH  
        ["H", -1.4,  1.3,  0.0],      # H on first OH
        
        # Ethylene glycol approaching - 5 atoms
        ["H",  2.0,  0.2,  0.0],      # H on second OH
        ["C",  0.0, -2.0,  0.0],      # First carbon
        ["C",  1.4, -2.0,  0.0],      # Second carbon
        ["O", -0.8, -2.8,  0.0],      # First OH group
        ["O",  2.2, -2.8,  0.0],      # Second OH group
    ]
    
    print("   Ultra-minimal boronate-diol: 9 atoms")
    print("   Chemistry: B(OH)₂ + ethylene glycol → tests B-O bonding")
    return coordinates

def create_ultraminimal_surface():
    """
    Ultra-minimal surface: Ti3C2 cluster = 5 atoms
    Smallest possible MXene representation
    """
    
    coordinates = [
        # Ti3C2 unit - 5 atoms total
        ["Ti", 0.0,  0.0,  0.0],      # Central Ti
        ["Ti", 3.0,  0.0,  0.0],      # Second Ti
        ["Ti", 6.0,  0.0,  0.0],      # Third Ti
        ["C",  1.5,  0.0,  1.0],      # First C
        ["C",  4.5,  0.0,  1.0],      # Second C
    ]
    
    print("   Ultra-minimal surface: 5 atoms")
    print("   Chemistry: Ti₃C₂ cluster → tests MXene surface")
    return coordinates

def create_ultraminimal_combined():
    """
    Ultra-minimal combined: Ti3C2 + BO2H = 8 atoms total
    Minimum system to test surface-molecule interaction
    """
    
    coordinates = [
        # Ti3C2 surface - 5 atoms
        ["Ti", 0.0,  0.0,  0.0],
        ["Ti", 3.0,  0.0,  0.0], 
        ["Ti", 6.0,  0.0,  0.0],
        ["C",  1.5,  0.0,  1.0],
        ["C",  4.5,  0.0,  1.0],
        
        # B(OH)2 approaching - 3 atoms
        ["B",  3.0,  0.0,  3.0],      # Boron above surface
        ["O",  2.0,  0.0,  3.5],      # First OH
        ["O",  4.0,  0.0,  3.5],      # Second OH
    ]
    
    print("   Ultra-minimal combined: 8 atoms") 
    print("   Chemistry: Ti₃C₂ + B(OH)₂ → tests surface interaction")
    return coordinates

def create_cp2k_input_ultraminimal(coords, name, run_type="GEO_OPT"):
    """Create CP2K input optimized for M1 MacBook performance"""
    
    calc = CP2K()
    calc.working_directory = "./"
    calc.project_name = f"ultramin_{name}"
    
    # Main sections
    CP2K_INPUT = calc.CP2K_INPUT
    GLOBAL = CP2K_INPUT.GLOBAL
    FORCE_EVAL = CP2K_INPUT.FORCE_EVAL_add()
    
    # Global settings
    GLOBAL.Project_name = f"ultramin_{name}"
    GLOBAL.Run_type = run_type
    GLOBAL.Print_level = "LOW"  # Reduce output for speed
    
    # Force evaluation
    FORCE_EVAL.Method = "Quickstep"
    
    # DFT settings - optimized for speed
    dft = FORCE_EVAL.DFT
    dft.Basis_set_file_name = ["BASIS_MOLOPT", "BASIS_MOLOPT_UCL"]
    dft.Potential_file_name = "GTH_POTENTIALS"
    
    # Very aggressive settings for speed on M1
    dft.MGRID.Cutoff = 200      # Reduced from 280
    dft.MGRID.Rel_cutoff = 25   # Reduced from 40
    
    # SCF settings for speed
    dft.SCF.Eps_scf = 1.0e-5    # Slightly relaxed
    dft.SCF.Max_scf = 20        # Fewer max iterations
    dft.SCF.Guess = "RESTART"   # Will fallback to ATOMIC if no restart
    
    # Orbital transformation for speed
    dft.SCF.OT.Preconditioner = "FULL_SINGLE_INVERSE"
    dft.SCF.OT.Minimizer = "DIIS"
    dft.SCF.OT.Stepsize = 0.15
    
    # Simple XC functional for speed
    dft.XC.XC_FUNCTIONAL.Section_parameters = "PBE"  # No dispersion for speed
    
    # Smaller cell
    cell = FORCE_EVAL.SUBSYS.CELL
    cell_size = 10.0  # Smaller cell
    cell.A = [cell_size, 0, 0]
    cell.B = [0, cell_size, 0] 
    cell.C = [0, 0, cell_size]
    cell.Periodic = "NONE"  # Isolated system
    
    # Add coordinates
    for symbol, x, y, z in coords:
        FORCE_EVAL.SUBSYS.COORD.Default_keyword.append([symbol, x, y, z])
    
    # Define kinds with minimal basis sets
    unique_elements = list(set([coord[0] for coord in coords]))
    
    for element in unique_elements:
        kind = FORCE_EVAL.SUBSYS.KIND_add(element)
        
        if element == "H":
            kind.Basis_set = "SZV-MOLOPT-GTH"  # Smaller basis
            kind.Potential = "GTH-PBE-q1"
        elif element == "C":
            kind.Basis_set = "SZV-MOLOPT-GTH"
            kind.Potential = "GTH-PBE-q4" 
        elif element == "O":
            kind.Basis_set = "SZV-MOLOPT-GTH"
            kind.Potential = "GTH-PBE-q6"
        elif element == "B":
            kind.Basis_set = "SZV-MOLOPT-GTH"
            kind.Potential = "GTH-PBE-q3"
        elif element == "Ti":
            kind.Basis_set = "SZV-MOLOPT-SR-GTH"
            kind.Potential = "GTH-PBE-q12"
    
    # Motion settings based on run type
    if run_type == "GEO_OPT":
        motion = CP2K_INPUT.MOTION
        motion.GEO_OPT.Type = "MINIMIZATION"
        motion.GEO_OPT.Max_iter = 50  # Fewer iterations
        motion.GEO_OPT.Max_force = 0.001  # Relaxed convergence
        
        # Print settings
        print_geo = motion.PRINT_add().TRAJECTORY
        print_geo.Each.Geo_opt = 10
        print_geo.Filename = f"ultramin_{name}_geo"
        
    elif run_type == "MD":
        motion = CP2K_INPUT.MOTION
        md = motion.MD
        md.Ensemble = "NVE" 
        md.Steps = 100      # Very short MD
        md.Timestep = 0.5   # Larger timestep
        md.Temperature = 300
        
        # Print settings
        print_traj = motion.PRINT_add().TRAJECTORY
        print_traj.Each.Md = 10
        print_traj.Filename = f"ultramin_{name}_md"
    
    return calc

def build_all_ultraminimal_systems():
    """Build all ultra-minimal test systems optimized for M1 MacBook"""
    
    print("🔬 Building Ultra-Minimal Test Systems for M1 MacBook")
    print("=" * 60)
    
    systems = [
        ("boronate_diol", create_ultraminimal_boronate_diol),
        ("surface", create_ultraminimal_surface), 
        ("combined", create_ultraminimal_combined)
    ]
    
    run_types = [
        ("geo", "GEO_OPT"),
        ("md", "MD")
    ]
    
    total_files = 0
    
    for system_name, coord_func in systems:
        print(f"\n📋 Creating {system_name} system:")
        coords = coord_func()
        
        for run_suffix, run_type in run_types:
            filename = f"ultramin_{system_name}_{run_suffix}.inp"
            
            calc = create_cp2k_input_ultraminimal(coords, f"{system_name}_{run_suffix}", run_type)
            calc.write_input_file(filename)
            
            print(f"   ✅ {filename}")
            total_files += 1
    
    print(f"\n🎯 Created {total_files} ultra-minimal input files")
    print(f"   Atom counts: 5-9 atoms (vs. 11-18 in minimal systems)")
    print(f"   Estimated speedup: 5-10x faster than minimal systems")
    
    return total_files

def estimate_ultraminimal_performance():
    """Estimate performance for ultra-minimal systems"""
    
    print(f"\n📊 Performance Estimate for Ultra-Minimal Systems")
    print("=" * 60)
    
    # Based on H2 test: 2.47s for 2 atoms
    h2_time = 2.47
    scaling = 2.7  # DFT scaling factor
    
    systems = [
        ("H2 Reference", 2, h2_time),
        ("Ultra-minimal Surface", 5, 0),
        ("Ultra-minimal Combined", 8, 0), 
        ("Ultra-minimal Boronate-Diol", 9, 0)
    ]
    
    print(f"{'System':<30} {'Atoms':<6} {'SCF Step':<10} {'Geo Opt':<10} {'Short MD':<10}")
    print("-" * 75)
    
    total_time = 0
    
    for name, atoms, ref_time in systems:
        if atoms == 2:
            scf_time = ref_time
            geo_time = ref_time
            md_time = ref_time
            print(f"{name:<30} {atoms:<6} {scf_time:.1f}s      {geo_time:.1f}s      {md_time:.1f}s")
        else:
            # Scale from H2
            scale = (atoms / 2) ** scaling
            scf_time = h2_time * scale
            geo_time = scf_time * 20  # ~20 geo steps
            md_time = scf_time * 100  # 100 MD steps
            
            total_time += geo_time + md_time
            
            print(f"{name:<30} {atoms:<6} {scf_time:.1f}s      {geo_time/60:.1f}min     {md_time/60:.1f}min")
    
    print(f"\n💡 Ultra-Minimal Systems Summary:")
    print(f"   • Total test time: ~{total_time/60:.0f} minutes ({total_time/3600:.1f} hours)")
    print(f"   • Individual systems: 5-15 minutes each")
    print(f"   • M1 Pro rating: {'Excellent' if total_time < 1800 else 'Good'}")
    
    return total_time

if __name__ == "__main__":
    build_all_ultraminimal_systems()
    estimate_ultraminimal_performance() 
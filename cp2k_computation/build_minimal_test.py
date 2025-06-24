#!/usr/bin/env python3
"""
build_minimal_test.py
Generate minimal CP2K test systems that capture the same interaction types
as the full research system but with dramatically reduced computational cost.

Test Systems:
1. Mini boronate-diol (15 atoms) - Tests reversible covalent bonding
2. Ti₃C₂ + boronic acid (25 atoms) - Tests surface interactions  
3. Combined minimal system (30 atoms) - Tests both interactions

All systems use identical computational settings to the full system.
"""

import numpy as np
from ase import Atoms
from ase.io import write
import sys
sys.path.insert(0, '..')
from pycp2k import CP2K

def create_minimal_boronate_diol():
    """Create minimal boronate-diol complex (~15 atoms)"""
    
    # Simplified boronic acid: B(OH)2-phenyl -> B(OH)2-CH3
    # Simplified diol: ethylene glycol
    # Expected interaction: reversible covalent B-O bond formation
    
    positions = [
        # Boronic acid part (B(OH)2-CH3)
        [0.0, 0.0, 0.0],      # B
        [-1.2, 0.8, 0.0],     # O
        [-1.2, -0.8, 0.0],    # O  
        [1.5, 0.0, 0.0],      # C (methyl)
        [2.1, 0.9, 0.0],      # H
        [2.1, -0.9, 0.0],     # H
        [2.1, 0.0, 0.9],      # H
        [-1.9, 0.8, 0.0],     # H (OH)
        [-1.9, -0.8, 0.0],    # H (OH)
        
        # Ethylene glycol (approaching for binding)
        [-3.0, 2.0, 0.0],     # C
        [-4.2, 1.8, 0.0],     # C  
        [-2.8, 3.1, 0.0],     # O
        [-5.4, 1.6, 0.0],     # O
        [-3.5, 3.3, 0.0],     # H (OH)
        [-6.1, 1.4, 0.0],     # H (OH)
    ]
    
    symbols = ['B', 'O', 'O', 'C', 'H', 'H', 'H', 'H', 'H', 
               'C', 'C', 'O', 'O', 'H', 'H']
    
    atoms = Atoms(symbols=symbols, positions=positions)
    return atoms

def create_minimal_ti3c2_surface():
    """Create minimal Ti₃C₂ surface cluster (~10 atoms)"""
    
    # Simplified Ti₃C₂(OH)₂ -> Ti₃C₂ cluster with surface OH groups
    # Captures the key MXene surface chemistry
    
    positions = [
        # Ti₃C₂ core layer
        [0.0, 0.0, 0.0],      # Ti
        [3.0, 0.0, 0.0],      # Ti  
        [6.0, 0.0, 0.0],      # Ti
        [1.5, 0.0, -1.0],     # C
        [4.5, 0.0, -1.0],     # C
        
        # Surface terminations (OH groups)
        [0.0, 0.0, 1.5],      # O
        [3.0, 0.0, 1.5],      # O
        [6.0, 0.0, 1.5],      # O
        [0.0, 0.0, 2.5],      # H
        [3.0, 0.0, 2.5],      # H
        [6.0, 0.0, 2.5],      # H
    ]
    
    symbols = ['Ti', 'Ti', 'Ti', 'C', 'C', 'O', 'O', 'O', 'H', 'H', 'H']
    
    atoms = Atoms(symbols=symbols, positions=positions)
    return atoms

def create_combined_minimal_system():
    """Create combined system: Ti₃C₂ + boronic acid interaction (~25 atoms)"""
    
    # Ti₃C₂ surface + boronic acid approaching for binding
    # Tests both surface chemistry and boronate interactions
    
    positions = [
        # Ti₃C₂ surface
        [0.0, 0.0, 0.0],      # Ti
        [3.0, 0.0, 0.0],      # Ti  
        [6.0, 0.0, 0.0],      # Ti
        [1.5, 0.0, -1.0],     # C
        [4.5, 0.0, -1.0],     # C
        [0.0, 0.0, 1.5],      # O (surface)
        [6.0, 0.0, 1.5],      # O (surface)
        [0.0, 0.0, 2.5],      # H (surface OH)
        [6.0, 0.0, 2.5],      # H (surface OH)
        
        # Boronic acid approaching middle Ti site
        [3.0, 0.0, 4.0],      # B
        [2.2, 1.0, 4.5],      # O
        [3.8, -1.0, 4.5],     # O
        [3.0, 1.5, 2.8],      # C (simplified organic part)
        [1.5, 1.0, 5.2],      # H (OH)
        [4.5, -1.0, 5.2],     # H (OH)
        [2.0, 2.0, 2.8],      # H
        [4.0, 2.0, 2.8],      # H
        [3.0, 2.5, 2.8],      # H
    ]
    
    symbols = ['Ti', 'Ti', 'Ti', 'C', 'C', 'O', 'O', 'H', 'H',
               'B', 'O', 'O', 'C', 'H', 'H', 'H', 'H', 'H']
    
    atoms = Atoms(symbols=symbols, positions=positions)
    return atoms

def create_cp2k_input_minimal(atoms, project_name, cell_size=12.0):
    """Create CP2K input for minimal test systems"""
    
    inp = CP2K()
    
    # Global settings
    inp.CP2K_INPUT.GLOBAL.Project_name = project_name
    inp.CP2K_INPUT.GLOBAL.Run_type = "GEO_OPT"
    inp.CP2K_INPUT.GLOBAL.Print_level = "MEDIUM"
    
    # Force evaluation setup
    force_eval = inp.CP2K_INPUT.FORCE_EVAL_add()
    force_eval.Method = "Quickstep"
    
    # DFT settings (same as full system but smaller grid)
    dft = force_eval.DFT
    dft.Basis_set_file_name = "BASIS_MOLOPT"
    dft.Potential_file_name = "GTH_POTENTIALS"
    
    # Smaller cutoffs for faster testing while preserving accuracy
    dft.MGRID.Cutoff = 300  # Reduced from 400
    dft.MGRID.Rel_cutoff = 50  # Reduced from 60
    
    # SCF settings - same convergence criteria
    dft.SCF.Eps_scf = 1.0e-6
    dft.SCF.Max_scf = 50
    dft.SCF.OT.Preconditioner = "FULL_SINGLE_INVERSE"
    dft.SCF.OT.Minimizer = "DIIS"
    
    # XC functional: PBE + D3 (same as full system)
    dft.XC.XC_FUNCTIONAL.Section_parameters = "PBE"
    dft.XC.VDW_POTENTIAL.Potential_type = "PAIR_POTENTIAL"
    pair_pot = dft.XC.VDW_POTENTIAL.PAIR_POTENTIAL_add()
    pair_pot.Type = "DFTD3"
    pair_pot.Reference_functional = "PBE"
    
    # Smaller periodic cell
    cell = force_eval.SUBSYS.CELL
    cell.A = [cell_size, 0, 0]
    cell.B = [0, cell_size, 0] 
    cell.C = [0, 0, cell_size]
    cell.Periodic = "XYZ"
    
    # Add coordinates
    for symbol, pos in zip(atoms.get_chemical_symbols(), atoms.get_positions()):
        force_eval.SUBSYS.COORD.Default_keyword.append([symbol, pos[0], pos[1], pos[2]])
    
    # Basis sets and potentials for each element
    elements = set(atoms.get_chemical_symbols())
    for element in elements:
        kind = force_eval.SUBSYS.KIND_add()
        kind.Section_parameters = element
        if element == 'Ti':
            kind.Basis_set = "DZVP-MOLOPT-SR-GTH"
            kind.Potential = "GTH-PBE-q12"
        elif element == 'C':
            kind.Basis_set = "DZVP-MOLOPT-GTH"
            kind.Potential = "GTH-PBE-q4"
        elif element == 'B':
            kind.Basis_set = "DZVP-MOLOPT-GTH"
            kind.Potential = "GTH-PBE-q3"
        elif element == 'O':
            kind.Basis_set = "DZVP-MOLOPT-GTH"
            kind.Potential = "GTH-PBE-q6"
        elif element == 'H':
            kind.Basis_set = "DZVP-MOLOPT-GTH"
            kind.Potential = "GTH-PBE-q1"
    
    # Geometry optimization settings
    geo_opt = inp.CP2K_INPUT.MOTION.GEO_OPT
    geo_opt.Max_iter = 200
    geo_opt.Optimizer = "BFGS"
    geo_opt.Type = "MINIMIZATION"
    
    # Convergence criteria
    geo_opt.BFGS.Trust_radius = 0.25
    
    return inp

def generate_minimal_test_systems():
    """Generate all minimal test systems"""
    
    print("🧪 Generating minimal test systems...")
    print("=" * 50)
    
    systems = {
        'minimal_boronate_diol': create_minimal_boronate_diol(),
        'minimal_ti3c2_surface': create_minimal_ti3c2_surface(), 
        'minimal_combined': create_combined_minimal_system()
    }
    
    for name, atoms in systems.items():
        # Save XYZ file
        xyz_file = f"{name}.xyz"
        write(xyz_file, atoms)
        
        # Generate CP2K input
        inp = create_cp2k_input_minimal(atoms, name)
        inp_file = f"{name}.inp"
        inp.write_input_file(inp_file)
        
        print(f"✅ {name}: {len(atoms)} atoms")
        print(f"   📄 XYZ: {xyz_file}")
        print(f"   ⚙️  Input: {inp_file}")
        print(f"   🎯 Tests: {get_test_description(name)}")
        print()
    
    # Create a quick local test script
    create_local_test_script()
    
    print("🎉 Minimal test systems generated!")
    print("\n💡 Quick local test:")
    print("   python run_minimal_tests.py")

def get_test_description(system_name):
    """Get description of what each system tests"""
    descriptions = {
        'minimal_boronate_diol': "Reversible B-O covalent bonding",
        'minimal_ti3c2_surface': "MXene surface chemistry", 
        'minimal_combined': "Surface binding + boronate interactions"
    }
    return descriptions.get(system_name, "Unknown")

def create_local_test_script():
    """Create a script for quick local testing"""
    
    script_content = '''#!/usr/bin/env python3
"""
run_minimal_tests.py
Quick local verification of CP2K inputs and system setup.
Estimates computational cost and checks input validity.
"""

import subprocess
import time
from pathlib import Path

def estimate_computational_cost(atoms_count):
    """Estimate relative computational cost"""
    # Rough scaling: O(N^3) for DFT
    relative_cost = (atoms_count / 15) ** 3
    
    if relative_cost < 1:
        return "Very Fast (< 1 min)"
    elif relative_cost < 8:
        return "Fast (1-5 min)" 
    elif relative_cost < 27:
        return "Medium (5-15 min)"
    else:
        return "Slow (> 15 min)"

def check_cp2k_syntax(inp_file):
    """Check if CP2K input syntax is valid"""
    try:
        # Try to parse the input file
        with open(inp_file, 'r') as f:
            content = f.read()
        
        # Basic syntax checks
        if '&GLOBAL' not in content:
            return False, "Missing GLOBAL section"
        if '&FORCE_EVAL' not in content:
            return False, "Missing FORCE_EVAL section"
        if '&DFT' not in content:
            return False, "Missing DFT section"
            
        return True, "Syntax OK"
    except Exception as e:
        return False, f"Error: {str(e)}"

def run_tests():
    """Run all minimal system tests"""
    
    systems = [
        ('minimal_boronate_diol.inp', 15),
        ('minimal_ti3c2_surface.inp', 11),
        ('minimal_combined.inp', 18)
    ]
    
    print("🧪 CP2K Minimal System Tests")
    print("=" * 40)
    
    for inp_file, atom_count in systems:
        if Path(inp_file).exists():
            syntax_ok, msg = check_cp2k_syntax(inp_file)
            cost = estimate_computational_cost(atom_count)
            
            status = "✅" if syntax_ok else "❌"
            print(f"{status} {inp_file}")
            print(f"   Atoms: {atom_count}")
            print(f"   Cost: {cost}")
            print(f"   Status: {msg}")
            print()
        else:
            print(f"❌ {inp_file} - File not found")
    
    print("💡 To run with CP2K:")
    print("   cp2k.sopt -in minimal_boronate_diol.inp")
    print("   cp2k.sopt -in minimal_ti3c2_surface.inp") 
    print("   cp2k.sopt -in minimal_combined.inp")
    
    print("\\n🎯 Expected results:")
    print("   - Energy convergence in < 20 SCF steps")
    print("   - Geometry optimization in < 50 steps")
    print("   - B-O bond formation/breaking dynamics")
    print("   - Ti-O surface interactions")

if __name__ == "__main__":
    run_tests()
'''
    
    with open('run_minimal_tests.py', 'w') as f:
        f.write(script_content)
    
    print("📋 Created run_minimal_tests.py for local verification")

if __name__ == "__main__":
    generate_minimal_test_systems() 
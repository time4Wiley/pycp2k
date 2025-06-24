#!/usr/bin/env python3
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
    
    print("\n🎯 Expected results:")
    print("   - Energy convergence in < 20 SCF steps")
    print("   - Geometry optimization in < 50 steps")
    print("   - B-O bond formation/breaking dynamics")
    print("   - Ti-O surface interactions")

if __name__ == "__main__":
    run_tests()

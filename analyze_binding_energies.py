#!/usr/bin/env python3
"""
Analyze binding energies from completed geometry optimization jobs.
Calculate and compare PVA-borate vs CBA-borate binding strengths.
"""

import re
import os

def extract_final_energy(output_file):
    """Extract final optimized energy from CP2K output."""
    if not os.path.exists(output_file):
        return None, f"File not found: {output_file}"
    
    try:
        with open(output_file, 'r') as f:
            content = f.read()
        
        # Check if geometry optimization completed
        if "GEOMETRY OPTIMIZATION COMPLETED" not in content:
            return None, "Geometry optimization not completed"
        
        # Extract final energy
        lines = content.split('\n')
        for line in reversed(lines):
            if "Total energy:" in line and "Hartree" not in line:
                energy_str = line.split()[-1]
                try:
                    energy = float(energy_str)
                    return energy, "Success"
                except ValueError:
                    continue
        
        return None, "Final energy not found"
        
    except Exception as e:
        return None, f"Error reading file: {e}"

def calculate_binding_energies():
    """Calculate binding energies for both systems."""
    
    # File paths
    pva_output = "energy_compare/01_pva_borate_geo_opt/pva_borate_geo_opt.out"
    cba_output = "energy_compare/02_cba_borate_geo_opt_improved/cba_borate_geo_opt_improved.out"
    
    print("🔬 **BINDING ENERGY ANALYSIS**")
    print("=" * 50)
    
    # Extract energies
    pva_energy, pva_status = extract_final_energy(pva_output)
    cba_energy, cba_status = extract_final_energy(cba_output)
    
    print(f"📊 **RESULTS:**")
    print(f"PVA-borate complex: {pva_energy:.6f} Hartree ({pva_status})")
    print(f"CBA-borate complex: {cba_energy:.6f} Hartree ({cba_status})")
    print("")
    
    if pva_energy is not None and cba_energy is not None:
        # Calculate energy difference
        energy_diff_hartree = cba_energy - pva_energy
        energy_diff_kcal = energy_diff_hartree * 627.5  # Hartree to kcal/mol
        
        print(f"🎯 **BINDING ENERGY COMPARISON:**")
        print(f"Energy difference (CBA - PVA): {energy_diff_hartree:.6f} Hartree")
        print(f"Energy difference (CBA - PVA): {energy_diff_kcal:.1f} kcal/mol")
        print("")
        
        if energy_diff_kcal > 0:
            print(f"✅ **PVA-borate is MORE STABLE** by {abs(energy_diff_kcal):.1f} kcal/mol")
            print("   → PVA forms stronger boronate bonds")
        else:
            print(f"✅ **CBA-borate is MORE STABLE** by {abs(energy_diff_kcal):.1f} kcal/mol")
            print("   → CBA forms stronger boronate bonds")
        
        print("")
        print(f"💡 **INTERPRETATION:**")
        if abs(energy_diff_kcal) > 10:
            print(f"   Strong preference ({abs(energy_diff_kcal):.1f} kcal/mol)")
        elif abs(energy_diff_kcal) > 3:
            print(f"   Moderate preference ({abs(energy_diff_kcal):.1f} kcal/mol)")
        else:
            print(f"   Similar binding strength ({abs(energy_diff_kcal):.1f} kcal/mol)")
        
        print("")
        print(f"🧪 **HYDROGEL DESIGN IMPLICATIONS:**")
        if energy_diff_kcal > 10:
            print("   → Use PVA for stronger, more stable hydrogels")
            print("   → PVA gels will have better mechanical properties")
        elif energy_diff_kcal < -10:
            print("   → Use CBA for stronger crosslinking")
            print("   → CBA provides superior gelation")
        else:
            print("   → Both polymers show similar binding")
            print("   → Choice can be based on other factors (cost, processability)")
            
    else:
        print("❌ **ERROR:** Cannot calculate binding energies")
        if pva_energy is None:
            print(f"   PVA issue: {pva_status}")
        if cba_energy is None:
            print(f"   CBA issue: {cba_status}")
    
    print("")
    print("📝 **NEXT STEPS:**")
    print("1. Update scientific reports with final results")
    print("2. Generate publication-quality energy comparison plots")
    print("3. Document optimized molecular geometries")
    print("4. Prepare experimental recommendations")

if __name__ == "__main__":
    calculate_binding_energies() 
"""
Analyze binding energies from completed geometry optimization jobs.
Calculate and compare PVA-borate vs CBA-borate binding strengths.
"""

import re
import os

def extract_final_energy(output_file):
    """Extract final optimized energy from CP2K output."""
    if not os.path.exists(output_file):
        return None, f"File not found: {output_file}"
    
    try:
        with open(output_file, 'r') as f:
            content = f.read()
        
        # Check if geometry optimization completed
        if "GEOMETRY OPTIMIZATION COMPLETED" not in content:
            return None, "Geometry optimization not completed"
        
        # Extract final energy
        lines = content.split('\n')
        for line in reversed(lines):
            if "Total energy:" in line and "Hartree" not in line:
                energy_str = line.split()[-1]
                try:
                    energy = float(energy_str)
                    return energy, "Success"
                except ValueError:
                    continue
        
        return None, "Final energy not found"
        
    except Exception as e:
        return None, f"Error reading file: {e}"

def calculate_binding_energies():
    """Calculate binding energies for both systems."""
    
    # File paths
    pva_output = "energy_compare/01_pva_borate_geo_opt/pva_borate_geo_opt.out"
    cba_output = "energy_compare/02_cba_borate_geo_opt_improved/cba_borate_geo_opt_improved.out"
    
    print("🔬 **BINDING ENERGY ANALYSIS**")
    print("=" * 50)
    
    # Extract energies
    pva_energy, pva_status = extract_final_energy(pva_output)
    cba_energy, cba_status = extract_final_energy(cba_output)
    
    print(f"📊 **RESULTS:**")
    print(f"PVA-borate complex: {pva_energy:.6f} Hartree ({pva_status})")
    print(f"CBA-borate complex: {cba_energy:.6f} Hartree ({cba_status})")
    print("")
    
    if pva_energy is not None and cba_energy is not None:
        # Calculate energy difference
        energy_diff_hartree = cba_energy - pva_energy
        energy_diff_kcal = energy_diff_hartree * 627.5  # Hartree to kcal/mol
        
        print(f"🎯 **BINDING ENERGY COMPARISON:**")
        print(f"Energy difference (CBA - PVA): {energy_diff_hartree:.6f} Hartree")
        print(f"Energy difference (CBA - PVA): {energy_diff_kcal:.1f} kcal/mol")
        print("")
        
        if energy_diff_kcal > 0:
            print(f"✅ **PVA-borate is MORE STABLE** by {abs(energy_diff_kcal):.1f} kcal/mol")
            print("   → PVA forms stronger boronate bonds")
        else:
            print(f"✅ **CBA-borate is MORE STABLE** by {abs(energy_diff_kcal):.1f} kcal/mol")
            print("   → CBA forms stronger boronate bonds")
        
        print("")
        print(f"💡 **INTERPRETATION:**")
        if abs(energy_diff_kcal) > 10:
            print(f"   Strong preference ({abs(energy_diff_kcal):.1f} kcal/mol)")
        elif abs(energy_diff_kcal) > 3:
            print(f"   Moderate preference ({abs(energy_diff_kcal):.1f} kcal/mol)")
        else:
            print(f"   Similar binding strength ({abs(energy_diff_kcal):.1f} kcal/mol)")
        
        print("")
        print(f"🧪 **HYDROGEL DESIGN IMPLICATIONS:**")
        if energy_diff_kcal > 10:
            print("   → Use PVA for stronger, more stable hydrogels")
            print("   → PVA gels will have better mechanical properties")
        elif energy_diff_kcal < -10:
            print("   → Use CBA for stronger crosslinking")
            print("   → CBA provides superior gelation")
        else:
            print("   → Both polymers show similar binding")
            print("   → Choice can be based on other factors (cost, processability)")
            
    else:
        print("❌ **ERROR:** Cannot calculate binding energies")
        if pva_energy is None:
            print(f"   PVA issue: {pva_status}")
        if cba_energy is None:
            print(f"   CBA issue: {cba_status}")
    
    print("")
    print("📝 **NEXT STEPS:**")
    print("1. Update scientific reports with final results")
    print("2. Generate publication-quality energy comparison plots")
    print("3. Document optimized molecular geometries")
    print("4. Prepare experimental recommendations")

if __name__ == "__main__":
    calculate_binding_energies() 
"""
Analyze binding energies from completed geometry optimization jobs.
Calculate and compare PVA-borate vs CBA-borate binding strengths.
"""

import re
import os

def extract_final_energy(output_file):
    """Extract final optimized energy from CP2K output."""
    if not os.path.exists(output_file):
        return None, f"File not found: {output_file}"
    
    try:
        with open(output_file, 'r') as f:
            content = f.read()
        
        # Check if geometry optimization completed
        if "GEOMETRY OPTIMIZATION COMPLETED" not in content:
            return None, "Geometry optimization not completed"
        
        # Extract final energy
        lines = content.split('\n')
        for line in reversed(lines):
            if "Total energy:" in line and "Hartree" not in line:
                energy_str = line.split()[-1]
                try:
                    energy = float(energy_str)
                    return energy, "Success"
                except ValueError:
                    continue
        
        return None, "Final energy not found"
        
    except Exception as e:
        return None, f"Error reading file: {e}"

def calculate_binding_energies():
    """Calculate binding energies for both systems."""
    
    # File paths
    pva_output = "energy_compare/01_pva_borate_geo_opt/pva_borate_geo_opt.out"
    cba_output = "energy_compare/02_cba_borate_geo_opt_improved/cba_borate_geo_opt_improved.out"
    
    print("🔬 **BINDING ENERGY ANALYSIS**")
    print("=" * 50)
    
    # Extract energies
    pva_energy, pva_status = extract_final_energy(pva_output)
    cba_energy, cba_status = extract_final_energy(cba_output)
    
    print(f"📊 **RESULTS:**")
    print(f"PVA-borate complex: {pva_energy:.6f} Hartree ({pva_status})")
    print(f"CBA-borate complex: {cba_energy:.6f} Hartree ({cba_status})")
    print("")
    
    if pva_energy is not None and cba_energy is not None:
        # Calculate energy difference
        energy_diff_hartree = cba_energy - pva_energy
        energy_diff_kcal = energy_diff_hartree * 627.5  # Hartree to kcal/mol
        
        print(f"🎯 **BINDING ENERGY COMPARISON:**")
        print(f"Energy difference (CBA - PVA): {energy_diff_hartree:.6f} Hartree")
        print(f"Energy difference (CBA - PVA): {energy_diff_kcal:.1f} kcal/mol")
        print("")
        
        if energy_diff_kcal > 0:
            print(f"✅ **PVA-borate is MORE STABLE** by {abs(energy_diff_kcal):.1f} kcal/mol")
            print("   → PVA forms stronger boronate bonds")
        else:
            print(f"✅ **CBA-borate is MORE STABLE** by {abs(energy_diff_kcal):.1f} kcal/mol")
            print("   → CBA forms stronger boronate bonds")
        
        print("")
        print(f"💡 **INTERPRETATION:**")
        if abs(energy_diff_kcal) > 10:
            print(f"   Strong preference ({abs(energy_diff_kcal):.1f} kcal/mol)")
        elif abs(energy_diff_kcal) > 3:
            print(f"   Moderate preference ({abs(energy_diff_kcal):.1f} kcal/mol)")
        else:
            print(f"   Similar binding strength ({abs(energy_diff_kcal):.1f} kcal/mol)")
        
        print("")
        print(f"🧪 **HYDROGEL DESIGN IMPLICATIONS:**")
        if energy_diff_kcal > 10:
            print("   → Use PVA for stronger, more stable hydrogels")
            print("   → PVA gels will have better mechanical properties")
        elif energy_diff_kcal < -10:
            print("   → Use CBA for stronger crosslinking")
            print("   → CBA provides superior gelation")
        else:
            print("   → Both polymers show similar binding")
            print("   → Choice can be based on other factors (cost, processability)")
            
    else:
        print("❌ **ERROR:** Cannot calculate binding energies")
        if pva_energy is None:
            print(f"   PVA issue: {pva_status}")
        if cba_energy is None:
            print(f"   CBA issue: {cba_status}")
    
    print("")
    print("📝 **NEXT STEPS:**")
    print("1. Update scientific reports with final results")
    print("2. Generate publication-quality energy comparison plots")
    print("3. Document optimized molecular geometries")
    print("4. Prepare experimental recommendations")

if __name__ == "__main__":
    calculate_binding_energies() 
"""
Analyze binding energies from completed geometry optimization jobs.
Calculate and compare PVA-borate vs CBA-borate binding strengths.
"""

import re
import os

def extract_final_energy(output_file):
    """Extract final optimized energy from CP2K output."""
    if not os.path.exists(output_file):
        return None, f"File not found: {output_file}"
    
    try:
        with open(output_file, 'r') as f:
            content = f.read()
        
        # Check if geometry optimization completed
        if "GEOMETRY OPTIMIZATION COMPLETED" not in content:
            return None, "Geometry optimization not completed"
        
        # Extract final energy
        lines = content.split('\n')
        for line in reversed(lines):
            if "Total energy:" in line and "Hartree" not in line:
                energy_str = line.split()[-1]
                try:
                    energy = float(energy_str)
                    return energy, "Success"
                except ValueError:
                    continue
        
        return None, "Final energy not found"
        
    except Exception as e:
        return None, f"Error reading file: {e}"

def calculate_binding_energies():
    """Calculate binding energies for both systems."""
    
    # File paths
    pva_output = "energy_compare/01_pva_borate_geo_opt/pva_borate_geo_opt.out"
    cba_output = "energy_compare/02_cba_borate_geo_opt_improved/cba_borate_geo_opt_improved.out"
    
    print("🔬 **BINDING ENERGY ANALYSIS**")
    print("=" * 50)
    
    # Extract energies
    pva_energy, pva_status = extract_final_energy(pva_output)
    cba_energy, cba_status = extract_final_energy(cba_output)
    
    print(f"📊 **RESULTS:**")
    print(f"PVA-borate complex: {pva_energy:.6f} Hartree ({pva_status})")
    print(f"CBA-borate complex: {cba_energy:.6f} Hartree ({cba_status})")
    print("")
    
    if pva_energy is not None and cba_energy is not None:
        # Calculate energy difference
        energy_diff_hartree = cba_energy - pva_energy
        energy_diff_kcal = energy_diff_hartree * 627.5  # Hartree to kcal/mol
        
        print(f"🎯 **BINDING ENERGY COMPARISON:**")
        print(f"Energy difference (CBA - PVA): {energy_diff_hartree:.6f} Hartree")
        print(f"Energy difference (CBA - PVA): {energy_diff_kcal:.1f} kcal/mol")
        print("")
        
        if energy_diff_kcal > 0:
            print(f"✅ **PVA-borate is MORE STABLE** by {abs(energy_diff_kcal):.1f} kcal/mol")
            print("   → PVA forms stronger boronate bonds")
        else:
            print(f"✅ **CBA-borate is MORE STABLE** by {abs(energy_diff_kcal):.1f} kcal/mol")
            print("   → CBA forms stronger boronate bonds")
        
        print("")
        print(f"💡 **INTERPRETATION:**")
        if abs(energy_diff_kcal) > 10:
            print(f"   Strong preference ({abs(energy_diff_kcal):.1f} kcal/mol)")
        elif abs(energy_diff_kcal) > 3:
            print(f"   Moderate preference ({abs(energy_diff_kcal):.1f} kcal/mol)")
        else:
            print(f"   Similar binding strength ({abs(energy_diff_kcal):.1f} kcal/mol)")
        
        print("")
        print(f"🧪 **HYDROGEL DESIGN IMPLICATIONS:**")
        if energy_diff_kcal > 10:
            print("   → Use PVA for stronger, more stable hydrogels")
            print("   → PVA gels will have better mechanical properties")
        elif energy_diff_kcal < -10:
            print("   → Use CBA for stronger crosslinking")
            print("   → CBA provides superior gelation")
        else:
            print("   → Both polymers show similar binding")
            print("   → Choice can be based on other factors (cost, processability)")
            
    else:
        print("❌ **ERROR:** Cannot calculate binding energies")
        if pva_energy is None:
            print(f"   PVA issue: {pva_status}")
        if cba_energy is None:
            print(f"   CBA issue: {cba_status}")
    
    print("")
    print("📝 **NEXT STEPS:**")
    print("1. Update scientific reports with final results")
    print("2. Generate publication-quality energy comparison plots")
    print("3. Document optimized molecular geometries")
    print("4. Prepare experimental recommendations")

if __name__ == "__main__":
    calculate_binding_energies() 
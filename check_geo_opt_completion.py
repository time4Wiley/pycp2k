#!/usr/bin/env python3
"""
Simple script to check geometry optimization completion and process results.
Run this after the SLURM jobs finish.
"""

import os
import re
import subprocess

def check_jobs_completed():
    """Check if geometry optimization jobs are still running"""
    try:
        result = subprocess.Popen(['squeue', '-u', 'acdad3pzwp'], 
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = result.communicate()
        stdout = stdout.decode('utf-8')
        
        geo_opt_jobs = []
        for line in stdout.split('\n')[1:]:  # Skip header
            if line.strip() and ('pva_borate_geo' in line or 'cba_borate_geo' in line):
                geo_opt_jobs.append(line.strip())
        return len(geo_opt_jobs) == 0, geo_opt_jobs
    except Exception as e:
        print(f"Error checking jobs: {e}")
        return False, []

def extract_final_geometry_and_energy(output_file):
    """Extract optimized geometry and final energy from CP2K output"""
    if not os.path.exists(output_file):
        return None, None
    
    try:
        with open(output_file, 'r') as f:
            content = f.read()
        
        # Check if optimization completed successfully
        if "GEOMETRY OPTIMIZATION COMPLETED" not in content:
            print(f"Warning: Geometry optimization may not have completed in {output_file}")
            return None, None
        
        # Extract final energy
        energy_pattern = r'ENERGY\|\s*Total FORCE_EVAL.*?(-?\d+\.\d+)'
        energy_matches = re.findall(energy_pattern, content)
        final_energy = float(energy_matches[-1]) if energy_matches else None
        
        # Extract final coordinates
        final_coords = []
        lines = content.split('\n')
        
        # Find the last occurrence of atomic coordinates
        coord_start = -1
        for i in range(len(lines)-1, -1, -1):
            if 'ATOMIC COORDINATES IN angstrom' in lines[i]:
                coord_start = i
                break
        
        if coord_start != -1:
            # Extract coordinates
            for i in range(coord_start + 4, len(lines)):  # Skip header lines
                line = lines[i].strip()
                if not line or line.startswith('-') or 'Sum of atomic charges' in line:
                    break
                parts = line.split()
                if len(parts) >= 5:  # Element, X, Y, Z, and possibly more
                    element = parts[1]
                    x, y, z = parts[2], parts[3], parts[4]
                    final_coords.append(f"{element}       {x}       {y}       {z}")
        
        return final_coords, final_energy
    
    except Exception as e:
        print(f"Error processing {output_file}: {e}")
        return None, None

def main():
    """Check completion status and process results"""
    
    # Check if jobs are still running
    completed, running_jobs = check_jobs_completed()
    
    if not completed:
        print("Geometry optimization jobs are still running:")
        for job in running_jobs:
            print(f"  {job}")
        print("\nRun this script again after jobs complete.")
        return
    
    print("All geometry optimization jobs have completed!")
    
    # Check results
    results = {}
    
    # PVA-borate results
    pva_output = "energy_compare/01_pva_borate_geo_opt/pva_borate_geo_opt.out"
    pva_coords, pva_energy = extract_final_geometry_and_energy(pva_output)
    results['pva'] = {'coords': pva_coords, 'energy': pva_energy, 'file': pva_output}
    
    # CBA-borate results
    cba_output = "energy_compare/02_cba_borate_geo_opt/cba_borate_geo_opt.out"
    cba_coords, cba_energy = extract_final_geometry_and_energy(cba_output)
    results['cba'] = {'coords': cba_coords, 'energy': cba_energy, 'file': cba_output}
    
    # Report results
    print("\n" + "="*60)
    print("GEOMETRY OPTIMIZATION RESULTS")
    print("="*60)
    
    for system, data in results.items():
        system_name = "PVA-borate" if system == 'pva' else "CBA-borate"
        print(f"\n{system_name}:")
        
        if data['coords'] and data['energy']:
            print(f"  ✓ Optimization successful")
            print(f"  ✓ Final energy: {data['energy']:.9f} au")
            print(f"  ✓ Optimized coordinates: {len(data['coords'])} atoms")
        else:
            print(f"  ✗ Failed to extract results from {data['file']}")
            if os.path.exists(data['file']):
                # Check file size to see if it's actually written
                size = os.path.getsize(data['file'])
                print(f"    Output file size: {size} bytes")
                if size == 0:
                    print("    Output file is empty - job may have failed")
            else:
                print(f"    Output file {data['file']} does not exist")
    
    # Calculate energy difference if both succeeded
    if results['pva']['energy'] and results['cba']['energy']:
        energy_diff = results['pva']['energy'] - results['cba']['energy']
        energy_diff_kcal = energy_diff * 627.509  # Convert au to kcal/mol
        
        print(f"\n" + "="*60)
        print("BINDING ENERGY COMPARISON (OPTIMIZED GEOMETRIES)")
        print("="*60)
        print(f"PVA-borate final energy:  {results['pva']['energy']:.9f} au")
        print(f"CBA-borate final energy:  {results['cba']['energy']:.9f} au")
        print(f"Energy difference:        {energy_diff:.9f} au")
        print(f"Energy difference:        {energy_diff_kcal:.2f} kcal/mol")
        
        if energy_diff < 0:
            print(f"\n✓ PVA-borate is MORE STABLE by {abs(energy_diff_kcal):.2f} kcal/mol")
        else:
            print(f"\n✓ CBA-borate is MORE STABLE by {energy_diff_kcal:.2f} kcal/mol")
        
        print(f"\nThis represents the binding energy difference with optimized geometries")
        print(f"compared to our previous placeholder calculation (45.58 kcal/mol difference)")
    
    print(f"\n" + "="*60)

if __name__ == "__main__":
    main() 
#!/usr/bin/env python3
"""
Monitor geometry optimization jobs and prepare final energy calculations
with optimized geometries for binding energy comparison.
"""

import os
import subprocess
import time
import re
from pathlib import Path

def check_job_status(job_ids):
    """Check the status of SLURM jobs"""
    try:
        result = subprocess.run(['squeue', '-u', 'acdad3pzwp'], 
                              capture_output=True, text=True)
        running_jobs = []
        for line in result.stdout.split('\n')[1:]:  # Skip header
            if line.strip():
                parts = line.split()
                if len(parts) >= 1:
                    job_id = parts[0]
                    if job_id in job_ids:
                        status = parts[4] if len(parts) > 4 else 'UNKNOWN'
                        time_running = parts[5] if len(parts) > 5 else '0:00'
                        running_jobs.append((job_id, status, time_running))
        return running_jobs
    except Exception as e:
        print(f"Error checking job status: {e}")
        return []

def extract_optimized_geometry(output_file):
    """Extract the final optimized geometry from CP2K output"""
    try:
        with open(output_file, 'r') as f:
            content = f.read()
        
        # Look for the final geometry section
        # CP2K prints optimized coordinates at the end
        final_coords = []
        lines = content.split('\n')
        
        # Find the last occurrence of atomic coordinates
        coord_start = -1
        for i in range(len(lines)-1, -1, -1):
            if 'ATOMIC COORDINATES IN angstrom' in lines[i]:
                coord_start = i
                break
        
        if coord_start == -1:
            print(f"Warning: Could not find final coordinates in {output_file}")
            return None
            
        # Extract coordinates starting after the header
        for i in range(coord_start + 4, len(lines)):  # Skip header lines
            line = lines[i].strip()
            if not line or line.startswith('-') or 'Sum of atomic charges' in line:
                break
            parts = line.split()
            if len(parts) >= 5:  # Element, X, Y, Z, and possibly more
                element = parts[1]
                x, y, z = parts[2], parts[3], parts[4]
                final_coords.append(f"{element}       {x}       {y}       {z}")
        
        return final_coords
    except Exception as e:
        print(f"Error extracting geometry from {output_file}: {e}")
        return None

def get_final_energy(output_file):
    """Extract the final energy from CP2K output"""
    try:
        with open(output_file, 'r') as f:
            content = f.read()
        
        # Look for the final energy
        energy_pattern = r'ENERGY\|\s*Total FORCE_EVAL.*?(-?\d+\.\d+)'
        matches = re.findall(energy_pattern, content)
        if matches:
            return float(matches[-1])  # Return the last (final) energy
        return None
    except Exception as e:
        print(f"Error extracting energy from {output_file}: {e}")
        return None

def create_final_energy_input(system_name, coords, charge, output_dir):
    """Create final single-point energy calculation with optimized geometry"""
    
    # Determine unique elements for KIND sections
    elements = set()
    for line in coords:
        if line.strip():
            elements.add(line.split()[0])
    
    # Create KIND sections
    kind_sections = ""
    for element in sorted(elements):
        if element == 'H':
            potential = "GTH-PBE-q1"
        elif element == 'C':
            potential = "GTH-PBE-q4"
        elif element == 'O':
            potential = "GTH-PBE-q6"
        elif element == 'B':
            potential = "GTH-PBE-q3"
        else:
            potential = f"GTH-PBE"  # fallback
            
        kind_sections += f"""    &KIND {element}
      POTENTIAL {potential}
      BASIS_SET DZVP-MOLOPT-SR-GTH
    &END KIND
"""
    
    coords_str = '\n'.join(coords)
    
    input_content = f"""&GLOBAL
  PRINT_LEVEL MEDIUM
  PROJECT_NAME {system_name}_final_energy
  RUN_TYPE ENERGY
&END GLOBAL

&FORCE_EVAL
  METHOD Quickstep
  &DFT
    POTENTIAL_FILE_NAME GTH_POTENTIALS
    CHARGE {charge}
    BASIS_SET_FILE_NAME BASIS_MOLOPT
    &SCF
      MAX_SCF 100
      EPS_SCF 1e-06
      SCF_GUESS ATOMIC
      &MIXING
        METHOD BROYDEN_MIXING
        ALPHA 0.4
        NBUFFER 8
      &END MIXING
    &END SCF
    &MGRID
      NGRIDS 4
      CUTOFF 400
      REL_CUTOFF 50
    &END MGRID
    &XC
      &XC_FUNCTIONAL
        &PBE
          SCALE_X 1.0
          SCALE_C 1.0
        &END PBE
      &END XC_FUNCTIONAL
    &END XC
  &END DFT
  &SUBSYS
    &CELL
      A 15.0 0.0 0.0
      B 0.0 15.0 0.0
      C 0.0 0.0 15.0
      PERIODIC NONE
    &END CELL
    &COORD
{coords_str}
    &END COORD
{kind_sections}  &END SUBSYS
&END FORCE_EVAL
"""
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Write input file
    input_file = os.path.join(output_dir, f"{system_name}_final_energy.inp")
    with open(input_file, 'w') as f:
        f.write(input_content)
    
    return input_file

def create_final_energy_slurm_job(system_name, input_file, output_dir):
    """Create SLURM job for final energy calculation"""
    
    job_script = f"""#!/bin/bash
#SBATCH --job-name={system_name}_final
#SBATCH --partition=xhacnormalc
#SBATCH --nodes=1
#SBATCH --ntasks=8
#SBATCH --time=01:00:00
#SBATCH --output={system_name}_final_%j.out
#SBATCH --error={system_name}_final_%j.err

# Load the working CP2K 2023.1 + Intel MPI module
module load cp2k-2023.1-intelmpi_2021

# Essential PMI library for proper MPI communication
export I_MPI_PMI_LIBRARY=/opt/gridview/slurm/lib/libpmi.so

# Set OpenMP threads
export OMP_NUM_THREADS=1

echo "Starting final energy calculation for {system_name}"
echo "Start time: $(date)"

cd $SLURM_SUBMIT_DIR

# Run CP2K energy calculation
srun --mpi=pmi2 cp2k.popt -i {input_file} -o {system_name}_final_energy.out

if [ $? -eq 0 ]; then
    echo "Final energy calculation completed successfully"
    echo "Final energy:"
    grep "ENERGY|" {system_name}_final_energy.out | tail -1
else
    echo "Final energy calculation failed with error code $?"
fi

echo "End time: $(date)"
"""
    
    job_file = os.path.join(output_dir, f"{system_name}_final_energy.slurm")
    with open(job_file, 'w') as f:
        f.write(job_script)
    os.chmod(job_file, 0o755)
    
    return job_file

def main():
    """Main monitoring and calculation setup function"""
    
    # Job IDs for geometry optimizations
    pva_job_id = "15269072"
    cba_job_id = "15269073"
    job_ids = [pva_job_id, cba_job_id]
    
    # Output files
    pva_output = "energy_compare/01_pva_borate_geo_opt/pva_borate_geo_opt.out"
    cba_output = "energy_compare/02_cba_borate_geo_opt/cba_borate_geo_opt.out"
    
    print("Monitoring geometry optimization jobs...")
    print(f"PVA-borate: Job {pva_job_id}")
    print(f"CBA-borate: Job {cba_job_id}")
    
    while True:
        running_jobs = check_job_status(job_ids)
        
        if not running_jobs:
            print("\nAll geometry optimization jobs completed!")
            break
        
        print(f"\nRunning jobs:")
        for job_id, status, time_running in running_jobs:
            system = "PVA-borate" if job_id == pva_job_id else "CBA-borate"
            print(f"  {system}: Job {job_id}, Status: {status}, Runtime: {time_running}")
        
        time.sleep(30)  # Check every 30 seconds
    
    print("\nProcessing completed geometry optimizations...")
    
    # Process PVA-borate results
    if os.path.exists(pva_output):
        print(f"\nProcessing PVA-borate results from {pva_output}")
        pva_coords = extract_optimized_geometry(pva_output)
        pva_geo_energy = get_final_energy(pva_output)
        
        if pva_coords:
            print(f"Extracted {len(pva_coords)} optimized coordinates for PVA-borate")
            if pva_geo_energy:
                print(f"Geometry optimization final energy: {pva_geo_energy:.9f} au")
            
            # Create final energy calculation
            final_dir = "energy_compare/03_pva_borate_final"
            pva_final_inp = create_final_energy_input("pva_borate", pva_coords, 0, final_dir)
            pva_final_job = create_final_energy_slurm_job("pva_borate", 
                                                         "pva_borate_final_energy.inp", 
                                                         final_dir)
            print(f"Created final energy input: {pva_final_inp}")
            print(f"Created final energy job: {pva_final_job}")
        else:
            print("Failed to extract PVA-borate optimized coordinates")
    
    # Process CBA-borate results
    if os.path.exists(cba_output):
        print(f"\nProcessing CBA-borate results from {cba_output}")
        cba_coords = extract_optimized_geometry(cba_output)
        cba_geo_energy = get_final_energy(cba_output)
        
        if cba_coords:
            print(f"Extracted {len(cba_coords)} optimized coordinates for CBA-borate")
            if cba_geo_energy:
                print(f"Geometry optimization final energy: {cba_geo_energy:.9f} au")
            
            # Create final energy calculation
            final_dir = "energy_compare/04_cba_borate_final"
            cba_final_inp = create_final_energy_input("cba_borate", cba_coords, -2, final_dir)
            cba_final_job = create_final_energy_slurm_job("cba_borate", 
                                                         "cba_borate_final_energy.inp", 
                                                         final_dir)
            print(f"Created final energy input: {cba_final_inp}")
            print(f"Created final energy job: {cba_final_job}")
        else:
            print("Failed to extract CBA-borate optimized coordinates")
    
    print(f"\nNext steps:")
    print(f"1. Submit final energy calculations:")
    print(f"   cd energy_compare/03_pva_borate_final && sbatch pva_borate_final_energy.slurm")
    print(f"   cd energy_compare/04_cba_borate_final && sbatch cba_borate_final_energy.slurm")
    print(f"2. Compare final optimized binding energies")

if __name__ == "__main__":
    main() 
#!/usr/bin/env python3
"""
Create Slurm job scripts for existing CP2K input files
Uses the hardened configuration: CP2K 2023.1 + Intel MPI + PMI2
"""

import os
import argparse


def create_slurm_script(input_dir, input_file, job_name, nodes=1, ntasks=4, time="2:00:00"):
    """Create a Slurm job script for CP2K calculation"""
    
    slurm_content = f"""#!/bin/bash
#SBATCH --job-name={job_name}
#SBATCH --partition=xhacnormalc
#SBATCH --nodes={nodes}
#SBATCH --ntasks-per-node={ntasks}
#SBATCH --cpus-per-task=1
#SBATCH --time={time}
#SBATCH --output={job_name}_%j.out
#SBATCH --error={job_name}_%j.err

# Hardened CP2K 2023.1 + Intel MPI configuration
module purge
module load cp2k-2023.1-intelmpi_2021

# Essential PMI library for Intel MPI + Slurm compatibility
export I_MPI_PMI_LIBRARY=/opt/gridview/slurm/lib/libpmi.so

# Change to job directory
cd $SLURM_SUBMIT_DIR

# Run CP2K with proven configuration
echo "Starting CP2K calculation: {job_name}"
echo "Input file: {input_file}"
echo "Working directory: $(pwd)"
echo "Number of MPI processes: $SLURM_NTASKS"

srun --mpi=pmi2 cp2k.popt -i {input_file} -o {job_name}.out

echo "CP2K calculation completed"
"""
    
    # Write Slurm script
    slurm_file = os.path.join(input_dir, "job.slurm")
    with open(slurm_file, "w") as f:
        f.write(slurm_content)
    
    # Make executable
    os.chmod(slurm_file, 0o755)
    
    return slurm_file


def main():
    """Create Slurm job scripts for binding energy calculations"""
    
    # PVA-borate job
    print("Creating Slurm job for PVA-borate calculation...")
    slurm1 = create_slurm_script(
        input_dir="energy_compare/01_pva_borate",
        input_file="bond_energy.inp", 
        job_name="pva_borate"
    )
    print(f"✓ Created: {slurm1}")
    
    # CBA-borate job  
    print("Creating Slurm job for CBA-borate calculation...")
    slurm2 = create_slurm_script(
        input_dir="energy_compare/02_cba_borate",
        input_file="bond_energy.inp",
        job_name="cba_borate"
    )
    print(f"✓ Created: {slurm2}")
    
    print("\n🎯 Slurm job scripts ready!")
    print("To submit:")
    print("  cd energy_compare/01_pva_borate && sbatch job.slurm")
    print("  cd energy_compare/02_cba_borate && sbatch job.slurm")


if __name__ == "__main__":
    main() 
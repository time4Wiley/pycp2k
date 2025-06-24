#!/usr/bin/env python3
"""
Create SLURM job scripts for CP2K geometry optimization calculations
using the hardened CP2K 2023.1 + Intel MPI configuration.
"""

import os

def create_slurm_job(system_name, input_file, output_dir, partition="xhacnormalc", nodes=1, ntasks=8, time="06:00:00"):
    """Create SLURM job script for CP2K geometry optimization"""
    
    job_script = f"""#!/bin/bash
#SBATCH --job-name={system_name}_geo_opt
#SBATCH --partition={partition}
#SBATCH --nodes={nodes}
#SBATCH --ntasks={ntasks}
#SBATCH --time={time}
#SBATCH --output={system_name}_geo_opt_%j.out
#SBATCH --error={system_name}_geo_opt_%j.err

# Load the working CP2K 2023.1 + Intel MPI module
module load cp2k-2023.1-intelmpi_2021

# Essential PMI library for proper MPI communication
export I_MPI_PMI_LIBRARY=/opt/gridview/slurm/lib/libpmi.so

# Set OpenMP threads (total cores / MPI processes)
export OMP_NUM_THREADS=1

# Print environment info
echo "Starting geometry optimization for {system_name}"
echo "CP2K version: $(cp2k.popt --version | head -1)"
echo "Input file: {input_file}"
echo "Number of MPI processes: $SLURM_NTASKS"
echo "Number of nodes: $SLURM_NNODES"
echo "Start time: $(date)"

# Change to working directory
cd $SLURM_SUBMIT_DIR

# Run CP2K geometry optimization using proven working configuration
srun --mpi=pmi2 cp2k.popt -i {input_file} -o {system_name}_geo_opt.out

# Check completion status
if [ $? -eq 0 ]; then
    echo "Geometry optimization completed successfully"
    echo "Output energy from final step:"
    grep "ENERGY|" {system_name}_geo_opt.out | tail -5
    echo "Optimization convergence:"
    grep -A5 "GEOMETRY OPTIMIZATION COMPLETED" {system_name}_geo_opt.out
else
    echo "Geometry optimization failed with error code $?"
fi

echo "End time: $(date)"
"""
    
    # Write job script
    job_file = os.path.join(output_dir, f"{system_name}_geo_opt.slurm")
    with open(job_file, 'w') as f:
        f.write(job_script)
    
    # Make executable
    os.chmod(job_file, 0o755)
    
    print(f"Created SLURM job script: {job_file}")
    return job_file

def main():
    """Generate SLURM job scripts for geometry optimizations"""
    
    # PVA-borate geometry optimization
    pva_dir = "energy_compare/01_pva_borate_geo_opt"
    pva_input = "pva_borate_geo_opt.inp"
    pva_job = create_slurm_job("pva_borate", pva_input, pva_dir, time="04:00:00")
    
    # CBA-borate geometry optimization  
    cba_dir = "energy_compare/02_cba_borate_geo_opt"
    cba_input = "cba_borate_geo_opt.inp"
    cba_job = create_slurm_job("cba_borate", cba_input, cba_dir, time="04:00:00")
    
    print(f"\nGenerated SLURM job scripts:")
    print(f"PVA-borate: {pva_job}")
    print(f"CBA-borate: {cba_job}")
    
    print(f"\nTo submit jobs:")
    print(f"cd {pva_dir} && sbatch pva_borate_geo_opt.slurm")
    print(f"cd {cba_dir} && sbatch cba_borate_geo_opt.slurm")
    
    print(f"\nEstimated runtime: 2-4 hours each")
    print(f"Jobs will generate optimized geometries and final energies")

if __name__ == "__main__":
    main() 
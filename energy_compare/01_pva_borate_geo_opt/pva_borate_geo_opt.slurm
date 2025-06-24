#!/bin/bash
#SBATCH --job-name=pva_borate_geo_opt
#SBATCH --partition=xhacnormalc
#SBATCH --nodes=1
#SBATCH --ntasks=8
#SBATCH --time=04:00:00
#SBATCH --output=pva_borate_geo_opt_%j.out
#SBATCH --error=pva_borate_geo_opt_%j.err

# Load the working CP2K 2023.1 + Intel MPI module
module load cp2k-2023.1-intelmpi_2021

# Essential PMI library for proper MPI communication
export I_MPI_PMI_LIBRARY=/opt/gridview/slurm/lib/libpmi.so

# Set OpenMP threads (total cores / MPI processes)
export OMP_NUM_THREADS=1

# Print environment info
echo "Starting geometry optimization for pva_borate"
echo "CP2K version: $(cp2k.popt --version | head -1)"
echo "Input file: pva_borate_geo_opt.inp"
echo "Number of MPI processes: $SLURM_NTASKS"
echo "Number of nodes: $SLURM_NNODES"
echo "Start time: $(date)"

# Change to working directory
cd $SLURM_SUBMIT_DIR

# Run CP2K geometry optimization using proven working configuration
srun --mpi=pmi2 cp2k.popt -i pva_borate_geo_opt.inp -o pva_borate_geo_opt.out

# Check completion status
if [ $? -eq 0 ]; then
    echo "Geometry optimization completed successfully"
    echo "Output energy from final step:"
    grep "ENERGY|" pva_borate_geo_opt.out | tail -5
    echo "Optimization convergence:"
    grep -A5 "GEOMETRY OPTIMIZATION COMPLETED" pva_borate_geo_opt.out
else
    echo "Geometry optimization failed with error code $?"
fi

echo "End time: $(date)"

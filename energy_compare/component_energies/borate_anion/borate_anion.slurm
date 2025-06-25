#!/bin/bash
#SBATCH --job-name=borate_anion
#SBATCH --partition=xhacnormalc
#SBATCH --nodes=1
#SBATCH --ntasks=4
#SBATCH --time=01:00:00
#SBATCH --output=borate_anion.out
#SBATCH --error=borate_anion.err

# Load CP2K module
module load cp2k-2023.1-intelmpi_2021

# Essential PMI library
export I_MPI_PMI_LIBRARY=/opt/gridview/slurm/lib/libpmi.so
export OMP_NUM_THREADS=1

echo "Starting borate_anion single point energy calculation"
echo "Job ID: $SLURM_JOB_ID"
echo "Start time: $(date)"

# Run CP2K
srun --mpi=pmi2 cp2k.popt -i borate_anion.inp -o borate_anion.out

if [ $? -eq 0 ]; then
    echo "✅ borate_anion completed successfully at $(date)"
    echo "Final energy:"
    grep "ENERGY|" borate_anion.out | tail -1
else
    echo "❌ borate_anion failed at $(date)"
fi

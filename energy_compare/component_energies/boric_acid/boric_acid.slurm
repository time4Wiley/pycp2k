#!/bin/bash
#SBATCH --job-name=boric_acid
#SBATCH --partition=xhacnormalc
#SBATCH --nodes=1
#SBATCH --ntasks=4
#SBATCH --time=01:00:00
#SBATCH --output=boric_acid.out
#SBATCH --error=boric_acid.err

# Load CP2K module
module load cp2k-2023.1-intelmpi_2021

# Essential PMI library
export I_MPI_PMI_LIBRARY=/opt/gridview/slurm/lib/libpmi.so
export OMP_NUM_THREADS=1

echo "Starting boric_acid single point energy calculation"
echo "Job ID: $SLURM_JOB_ID"
echo "Start time: $(date)"

# Run CP2K
srun --mpi=pmi2 cp2k.popt -i boric_acid.inp -o boric_acid.out

if [ $? -eq 0 ]; then
    echo "✅ boric_acid completed successfully at $(date)"
    echo "Final energy:"
    grep "ENERGY|" boric_acid.out | tail -1
else
    echo "❌ boric_acid failed at $(date)"
fi

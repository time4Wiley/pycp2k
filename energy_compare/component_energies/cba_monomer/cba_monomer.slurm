#!/bin/bash
#SBATCH --job-name=cba_monomer
#SBATCH --partition=xhacnormalc
#SBATCH --nodes=1
#SBATCH --ntasks=4
#SBATCH --time=01:00:00
#SBATCH --output=cba_monomer.out
#SBATCH --error=cba_monomer.err

# Load CP2K module
module load cp2k-2023.1-intelmpi_2021

# Essential PMI library
export I_MPI_PMI_LIBRARY=/opt/gridview/slurm/lib/libpmi.so
export OMP_NUM_THREADS=1

echo "Starting cba_monomer single point energy calculation"
echo "Job ID: $SLURM_JOB_ID"
echo "Start time: $(date)"

# Run CP2K
srun --mpi=pmi2 cp2k.popt -i cba_monomer.inp -o cba_monomer.out

if [ $? -eq 0 ]; then
    echo "✅ cba_monomer completed successfully at $(date)"
    echo "Final energy:"
    grep "ENERGY|" cba_monomer.out | tail -1
else
    echo "❌ cba_monomer failed at $(date)"
fi

#!/bin/bash
#SBATCH --job-name=cba_borate_freq
#SBATCH --partition=xhacnormalc
#SBATCH --nodes=1
#SBATCH --ntasks=8
#SBATCH --time=03:00:00
#SBATCH --output=cba_borate_freq.out
#SBATCH --error=cba_borate_freq.err

# Load CP2K module
module load cp2k-2023.1-intelmpi_2021

# Essential PMI library
export I_MPI_PMI_LIBRARY=/opt/gridview/slurm/lib/libpmi.so
export OMP_NUM_THREADS=1

echo "Starting cba_borate frequency analysis"
echo "Job ID: $SLURM_JOB_ID"
echo "Start time: $(date)"

# Run CP2K
srun --mpi=pmi2 cp2k.popt -i cba_borate_freq.inp -o cba_borate_freq.out

if [ $? -eq 0 ]; then
    echo "✅ cba_borate frequency analysis completed at $(date)"
    echo "Number of negative frequencies:"
    grep -c "VIB|Frequency.*-" cba_borate_freq.out || echo "0"
    echo "Lowest frequency:"
    grep "VIB|Frequency" cba_borate_freq.out | head -1
else
    echo "❌ cba_borate frequency analysis failed at $(date)"
fi

#!/bin/bash
#SBATCH -J cp2k_h2o_working
#SBATCH -p xhacnormalc
#SBATCH -N 1
#SBATCH --ntasks-per-node=8
#SBATCH -t 00:30:00
#SBATCH -o %x-%j.out
#SBATCH -e %x-%j.err

module purge
module load cp2k-2023.1-intelmpi_2021

export I_MPI_PMI_LIBRARY=/opt/gridview/slurm/lib/libpmi.so

echo "=== Working CP2K Test ==="
echo "Job started: $(date)"

srun --mpi=pmi2 cp2k.popt -i h2o.inp -o h2o_working.out

echo "Job completed: $(date)" 
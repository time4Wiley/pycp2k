#!/bin/bash
#SBATCH -J cba_borate_energy
#SBATCH -p xhacnormalc
#SBATCH -N 1
#SBATCH --ntasks-per-node=8
#SBATCH -t 02:00:00
#SBATCH -o %x-%j.out
#SBATCH -e %x-%j.err

module purge
module load cp2k-2023.1-intelmpi_2021

export I_MPI_PMI_LIBRARY=/opt/gridview/slurm/lib/libpmi.so

echo "=== CBA-Borate Bond Energy Calculation ==="
echo "Job started: $(date)"

srun --mpi=pmi2 cp2k.popt -i bond_energy.inp -o bond_energy.out

echo "Job completed: $(date)" 
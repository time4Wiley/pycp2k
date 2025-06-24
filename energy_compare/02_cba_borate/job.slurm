#!/bin/bash
#SBATCH --job-name=cba_borate
#SBATCH --partition=xhacnormalc
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=32
#SBATCH --cpus-per-task=2
#SBATCH --time=00:30:00
#SBATCH --output=cba_borate_%j.out
#SBATCH --error=cba_borate_%j.err
#SBATCH --mpi=pmix_v3

module purge
module load cp2k-2024.1-gcc-930-nopython

export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK

srun --mpi=pmix_v3 cp2k.psmp -in bond_energy.inp -o bond_energy.out 
#!/bin/bash
#SBATCH --job-name=pva_borate
#SBATCH --partition=xhacnormalc
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=8
#SBATCH --cpus-per-task=8
#SBATCH --time=00:30:00
#SBATCH --output=pva_borate_%j.out
#SBATCH --error=pva_borate_%j.err

module purge
module load cp2k-2024.1-gcc-930-nopython

export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK

srun cp2k.psmp -in bond_energy.inp -o bond_energy.out 
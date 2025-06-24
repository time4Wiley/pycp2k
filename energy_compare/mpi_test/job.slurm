#!/bin/bash
#SBATCH --job-name=cp2k_mpi_test
#SBATCH --partition=xhacnormalc
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=32
#SBATCH --cpus-per-task=2
#SBATCH --time=00:05:00
#SBATCH --output=mpi_test_%j.out
#SBATCH --error=mpi_test_%j.err

module purge
module load cp2k-2024.1-gcc-930-nopython

export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK

srun --mpi=pmix_v3 cp2k.psmp -in h2o.inp -o h2o.out 
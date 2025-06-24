#!/bin/bash
#SBATCH -J cp2k_h2o_gcc_test
#SBATCH -p xhacnormalc
#SBATCH -N 1
#SBATCH --ntasks-per-node=4       # 4 MPI ranks per node
#SBATCH --cpus-per-task=2         # 2 threads per rank
#SBATCH -t 00:30:00
#SBATCH -o %x-%j.out
#SBATCH -e %x-%j.err

module purge
module load cp2k-2024.1-gcc-930-nopython

export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK   # 2
# OpenMPI specific environment variables
export OMPI_MCA_btl_vader_single_copy_mechanism=none
export OMPI_MCA_mpi_warn_on_fork=0

echo "=== Module List ==="
module list

echo "=== Environment ==="
echo "OMP_NUM_THREADS=$OMP_NUM_THREADS" 
echo "SLURM_NTASKS=$SLURM_NTASKS"
echo "SLURM_CPUS_PER_TASK=$SLURM_CPUS_PER_TASK"

echo "=== Starting CP2K ==="
srun cp2k.psmp -i h2o.inp -o h2o_gcc.out

echo "=== Job Complete ===" 
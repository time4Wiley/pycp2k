#!/bin/bash
#SBATCH -J cp2k_h2o_intel_test
#SBATCH -p xhacnormalc
#SBATCH -N 1
#SBATCH --ntasks-per-node=4       # 4 MPI ranks per node
#SBATCH --cpus-per-task=2         # 2 threads per rank  
#SBATCH -t 00:30:00
#SBATCH -o %x-%j.out
#SBATCH -e %x-%j.err

module purge
module load compiler/intel/2021.3.0
module load mpi/intelmpi/2021.3.0
module load cp2k/2024.1-intelmpi-2021

export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK   # 2
export MKL_NUM_THREADS=$OMP_NUM_THREADS
export KMP_AFFINITY=granularity=fine,compact,1,0

echo "=== Module List ==="
module list

echo "=== Environment ==="
echo "OMP_NUM_THREADS=$OMP_NUM_THREADS"
echo "MKL_NUM_THREADS=$MKL_NUM_THREADS"
echo "SLURM_NTASKS=$SLURM_NTASKS"
echo "SLURM_CPUS_PER_TASK=$SLURM_CPUS_PER_TASK"

echo "=== Starting CP2K ==="
srun --mpi=pmix_v3 cp2k.psmp -i h2o.inp -o h2o_intel.out

echo "=== Job Complete ===" 
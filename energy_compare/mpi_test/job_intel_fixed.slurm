#!/bin/bash
#SBATCH -J cp2k_intel_direct
#SBATCH -p xhacnormalc
#SBATCH -N 1
#SBATCH --ntasks-per-node=4
#SBATCH --cpus-per-task=2
#SBATCH -t 00:30:00
#SBATCH -o %x-%j.out
#SBATCH -e %x-%j.err

module purge
module load compiler/intel/2021.3.0
module load mpi/intelmpi/2021.3.0
module load cp2k/2024.1-intelmpi-2021

export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK
export MKL_NUM_THREADS=$OMP_NUM_THREADS

echo "=== Testing Intel MPI without PMIx ==="
echo "Job started: $(date)"

# Try direct mpirun instead of srun
mpirun -np $SLURM_NTASKS cp2k.psmp -i h2o.inp -o h2o_intel_direct.out

echo "Job completed: $(date)" 
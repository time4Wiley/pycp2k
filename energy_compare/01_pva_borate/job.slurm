#!/bin/bash
#SBATCH -J pva_borate_energy
#SBATCH -p xhacnormalc
#SBATCH -N 1
#SBATCH --ntasks-per-node=8       # 8 MPI ranks per node
#SBATCH --cpus-per-task=2         # 2 threads per rank  
#SBATCH -t 02:00:00
#SBATCH -o %x-%j.out
#SBATCH -e %x-%j.err

module purge
module load compiler/intel/2021.3.0
module load mpi/intelmpi/2021.3.0
module load cp2k/2024.1-intelmpi-2021

export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK   # 2
export MKL_NUM_THREADS=$OMP_NUM_THREADS
export KMP_AFFINITY=granularity=fine,compact,1,0

echo "=== PVA-Borate Bond Energy Calculation ==="
echo "Job started: $(date)"

srun --mpi=pmix_v3 cp2k.psmp -i bond_energy.inp -o bond_energy.out

echo "Job completed: $(date)" 
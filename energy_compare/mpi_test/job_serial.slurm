#!/bin/bash
#SBATCH -J cp2k_serial_test
#SBATCH -p xhacnormalc
#SBATCH -N 1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH -t 00:30:00
#SBATCH -o %x-%j.out
#SBATCH -e %x-%j.err

module purge
module load cp2k-2024.1-gcc-930-nopython

export OMP_NUM_THREADS=1

echo "=== Serial CP2K Test ==="
echo "Job started: $(date)"
echo "Using single core to avoid MPI issues"

# Use cp2k.sopt (serial optimized) instead of cp2k.psmp (parallel)
cp2k.sopt -i h2o.inp -o h2o_serial.out

echo "Job completed: $(date)" 
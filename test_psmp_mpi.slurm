#!/bin/bash
#SBATCH --job-name=cp2k_psmp_test
#SBATCH --partition=xhacnormalc
#SBATCH --nodes=1
#SBATCH --ntasks=2
#SBATCH --cpus-per-task=1
#SBATCH --time=00:10:00
#SBATCH --output=psmp_test_%j.out
#SBATCH --error=psmp_test_%j.err

# Load required modules
module purge
module load cp2k-2024.1-gcc-930-nopython
module load anaconda3/2023.09

# Set up OpenMPI environment matching CP2K build
export PATH="/public/software/mpi/openmpi/4.1.5/bin:$PATH"
export LD_LIBRARY_PATH="/public/software/mpi/openmpi/4.1.5/lib:$LD_LIBRARY_PATH"

# Print environment info
echo "=== CP2K PSMP MPI Test ==="
echo "Job ID: $SLURM_JOB_ID"
echo "Nodes: $SLURM_JOB_NUM_NODES"
echo "Tasks: $SLURM_NTASKS"
echo "CP2K executable: $(which cp2k.psmp)"
echo "MPI run: $(which mpirun)"
echo "OpenMPI version: $(mpirun --version | head -1)"
echo

# Test direct execution (no MPI - should work)
echo "=== Test 1: Direct CP2K PSMP execution ==="
cp2k.psmp -i h2_psmp_test.inp -o h2_direct.out &
DIRECT_PID=$!

# Test MPI execution (if supported)
echo "=== Test 2: MPI CP2K PSMP execution ==="
mpirun -np $SLURM_NTASKS cp2k.psmp -i h2_psmp_test.inp -o h2_mpi.out &
MPI_PID=$!

# Wait for jobs to complete or timeout
timeout 300 wait $DIRECT_PID
timeout 300 wait $MPI_PID

echo "=== Results ==="
if [ -f "h2_direct.out" ]; then
    echo "✅ Direct execution completed"
    tail -5 h2_direct.out
else
    echo "❌ Direct execution failed"
fi

if [ -f "h2_mpi.out" ]; then
    echo "✅ MPI execution completed"
    tail -5 h2_mpi.out
else
    echo "❌ MPI execution failed"
fi

echo "=== Job completed ==="


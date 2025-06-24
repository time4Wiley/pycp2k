#!/bin/bash
#SBATCH --job-name=pycp2k_test
#SBATCH --partition=xhacnormalc
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=4
#SBATCH --time=00:10:00
#SBATCH --output=pycp2k_test_%j.out
#SBATCH --error=pycp2k_test_%j.err

echo "=== PyCP2K SLURM Test with CP2K 2024.1 ==="
echo "Job ID: $SLURM_JOB_ID"
echo "Node: $SLURM_NODELIST"
echo "Tasks: $SLURM_NTASKS"
echo "Date: $(date)"

# Load CP2K 2024.1 - NO GLIBC ISSUES!
module load cp2k-2024.1-gcc-930-nopython
module load anaconda3/2023.09

echo "CP2K_DATA_DIR: $CP2K_DATA_DIR"
echo "CP2K executable: $(which cp2k.psmp)"

# Run CP2K with MPI
echo "Starting CP2K calculation..."
mpirun -np $SLURM_NTASKS cp2k.psmp -i cp2k_slurm.inp -o cp2k_slurm.out

# Check results
if [ -f cp2k_slurm.out ]; then
    echo "=== Calculation completed ==="
    if grep -q "ENERGY| Total FORCE_EVAL" cp2k_slurm.out; then
        echo "✅ SUCCESS: Energy calculation completed!"
        grep "ENERGY| Total FORCE_EVAL" cp2k_slurm.out | tail -1
    else
        echo "⚠️ Calculation may not have finished"
        tail -20 cp2k_slurm.out
    fi
    
    echo "=== Timing Info ==="
    grep "CP2K                                 " cp2k_slurm.out || echo "No timing found"
    
    echo "=== Basis Set Confirmation ==="
    grep -i "basis.*molopt" cp2k_slurm.out | head -3 || echo "Basis set info not found"
    grep -i "potential.*gth" cp2k_slurm.out | head -3 || echo "Potential info not found"
else
    echo "❌ No output file found!"
    ls -la
fi

echo "Job completed at $(date)"

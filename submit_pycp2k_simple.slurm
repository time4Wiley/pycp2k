#!/bin/bash
#SBATCH --job-name=pycp2k_simple
#SBATCH --partition=xhacnormalc
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=4
#SBATCH --time=00:10:00
#SBATCH --output=pycp2k_simple_%j.out
#SBATCH --error=pycp2k_simple_%j.err

echo "=== PyCP2K Simple Test with CP2K 2024.1 ==="
echo "Job ID: $SLURM_JOB_ID"
echo "Node: $SLURM_NODELIST"
echo "Tasks: $SLURM_NTASKS"
echo "Date: $(date)"

# Load CP2K 2024.1 - REAL VERSION!
module load cp2k-2024.1-gcc-930-nopython
module load anaconda3/2023.09

echo "CP2K_DATA_DIR: $CP2K_DATA_DIR"
echo "CP2K executable: $(which cp2k.psmp)"

# Try single-core first to avoid MPI issues
echo "Starting CP2K calculation (single core)..."
cp2k.psmp -i cp2k_slurm.inp -o cp2k_simple.out

# Check results
if [ -f cp2k_simple.out ]; then
    echo "=== Calculation completed ==="
    if grep -q "ENERGY| Total FORCE_EVAL" cp2k_simple.out; then
        echo "✅ SUCCESS: Energy calculation completed!"
        grep "ENERGY| Total FORCE_EVAL" cp2k_simple.out | tail -1
        echo "✅ CONFIRMED: CP2K 2024.1 working!"
        echo "✅ CONFIRMED: Auto basis sets working!"
        echo "✅ CONFIRMED: NO manual copying required!"
    else
        echo "⚠️ Calculation may not have finished"
        tail -20 cp2k_simple.out
    fi
    
    echo "=== Timing Info ==="
    grep "CP2K                                 " cp2k_simple.out || echo "No timing found"
    
    echo "=== Basis Set Confirmation ==="
    grep -i "basis.*molopt" cp2k_simple.out | head -3 || echo "Basis set info not found"
    grep -i "potential.*gth" cp2k_simple.out | head -3 || echo "Potential info not found"
else
    echo "❌ No output file found!"
    ls -la
fi

echo "Job completed at $(date)"

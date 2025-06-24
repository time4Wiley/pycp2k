#!/bin/bash
#SBATCH --job-name=cba_borate_geo_opt_fixed
#SBATCH --partition=xhacnormalc
#SBATCH --nodes=1
#SBATCH --ntasks=8
#SBATCH --time=06:00:00
#SBATCH --output=cba_borate_geo_opt_fixed_%j.out
#SBATCH --error=cba_borate_geo_opt_fixed_%j.err

# Load the working CP2K 2023.1 + Intel MPI module
module load cp2k-2023.1-intelmpi_2021

# Essential PMI library for proper MPI communication
export I_MPI_PMI_LIBRARY=/opt/gridview/slurm/lib/libpmi.so

# Set OpenMP threads (total cores / MPI processes)
export OMP_NUM_THREADS=1

# Print environment info (without hanging --version command)
echo "Starting geometry optimization for cba_borate"
echo "Input file: cba_borate_geo_opt.inp"
echo "Number of MPI processes: $SLURM_NTASKS"
echo "Number of nodes: $SLURM_NNODES"
echo "Start time: $(date)"
echo "Working directory: $(pwd)"

# Change to working directory
cd $SLURM_SUBMIT_DIR

# Test if CP2K module loaded properly by checking if executable exists
if command -v cp2k.popt >/dev/null 2>&1; then
    echo "CP2K executable found: $(which cp2k.popt)"
else
    echo "ERROR: CP2K executable not found!"
    exit 1
fi

# Run CP2K geometry optimization using proven working configuration
echo "Starting CP2K calculation..."
srun --mpi=pmi2 cp2k.popt -i cba_borate_geo_opt.inp -o cba_borate_geo_opt.out

# Check completion status
exit_code=$?
if [ $exit_code -eq 0 ]; then
    echo "Geometry optimization completed successfully"
    echo "Final output file size: $(ls -lh cba_borate_geo_opt.out | awk '{print $5}')"
    if [ -f cba_borate_geo_opt.out ]; then
        echo "Last few energy lines:"
        grep "ENERGY|" cba_borate_geo_opt.out | tail -3
        echo "Checking convergence status:"
        if grep -q "GEOMETRY OPTIMIZATION COMPLETED" cba_borate_geo_opt.out; then
            echo "✅ GEOMETRY OPTIMIZATION CONVERGED"
        elif grep -q "MAXIMUM NUMBER OF OPTIMIZATION STEPS REACHED" cba_borate_geo_opt.out; then
            echo "⚠️  MAXIMUM STEPS REACHED - CHECK CONVERGENCE"
        else
            echo "🔄 OPTIMIZATION STATUS UNCLEAR - CHECK OUTPUT"
        fi
    fi
else
    echo "❌ Geometry optimization failed with exit code $exit_code"
fi

echo "End time: $(date)"
echo "Job completed"

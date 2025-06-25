#!/bin/bash
#SBATCH --job-name=h2o_single_point_test
#SBATCH --output=h2o_single_point_test.out
#SBATCH --error=h2o_single_point_test.err
#SBATCH --time=1:00:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=4
#SBATCH --cpus-per-task=1
#SBATCH --mem=8192M
#SBATCH --partition=xhacnormalc

# Job information
echo "Job ID: $SLURM_JOB_ID"
echo "Job Name: $SLURM_JOB_NAME"
echo "Node List: $SLURM_JOB_NODELIST"
echo "Number of nodes: $SLURM_JOB_NUM_NODES"
echo "Number of tasks: $SLURM_NTASKS"
echo "CPUs per task: $SLURM_CPUS_PER_TASK"
echo "Working directory: $(pwd)"
echo "Started at: $(date)"
echo

# Environment setup
module purge
# Load default modules - adapt these to your HPC environment
module load compiler/intel/2021.3.0
module load mpi/intelmpi/2021.3.0
module load cp2k-2023.1-intelmpi_2021

# Set environment variables for MPI
export I_MPI_PMI_LIBRARY=/opt/gridview/slurm/lib/libpmi2.so
export I_MPI_PMI=pmi2
export I_MPI_FABRICS=shm:ofi
export I_MPI_OFI_PROVIDER=verbs

# Verify CP2K is available
echo "CP2K executable: $(which cp2k.popt)"
cp2k.popt --version | head -3
echo

# Create output directory if needed
mkdir -p "$(dirname h2o_single_point_test.out)"

# Run CP2K
echo "Starting CP2K calculation..."
echo "Input file: h2o_single_point_test.inp"
echo "Output file: h2o_single_point_test.out"
echo "Command: mpirun -np $SLURM_NTASKS cp2k.popt -i h2o_single_point_test.inp -o h2o_single_point_test.out"
echo

mpirun -np $SLURM_NTASKS cp2k.popt -i h2o_single_point_test.inp -o h2o_single_point_test.out

# Capture exit code
CP2K_EXIT_CODE=$?

echo
echo "CP2K finished with exit code: $CP2K_EXIT_CODE"
echo "Finished at: $(date)"

# Job summary
echo
echo "=== JOB SUMMARY ==="
echo "Job ID: $SLURM_JOB_ID"
echo "Exit code: $CP2K_EXIT_CODE"
echo "Input file: h2o_single_point_test.inp"
echo "Output file: h2o_single_point_test.out"
echo "Runtime: $SECONDS seconds"

# Check if output file was created and has content
if [ -f "h2o_single_point_test.out" ] && [ -s "h2o_single_point_test.out" ]; then
    echo "Output file created successfully ($(wc -l < h2o_single_point_test.out) lines)"
    
    # Check for completion markers
    if grep -q "PROGRAM ENDED AT" "h2o_single_point_test.out"; then
        echo "CP2K calculation completed normally"
    elif grep -q "ABORT" "h2o_single_point_test.out"; then
        echo "WARNING: CP2K calculation aborted"
        CP2K_EXIT_CODE=1
    else
        echo "WARNING: CP2K calculation may not have completed normally"
    fi
else
    echo "ERROR: Output file not created or empty"
    CP2K_EXIT_CODE=1
fi

exit $CP2K_EXIT_CODE 
#!/bin/bash
#SBATCH --job-name=water_geo_opt_demo
#SBATCH --output=
#SBATCH --error=
#SBATCH --time=1:00:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=4
#SBATCH --cpus-per-task=1

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
module load intel/2023.1
module load intel-mpi/2021.9
module load cp2k/2023.1

# Set environment variables for MPI
export I_MPI_PMI_LIBRARY=/opt/gridview/slurm/lib/libpmi2.so
export I_MPI_PMI=pmi2
export I_MPI_FABRICS=shm:ofi
export I_MPI_OFI_PROVIDER=verbs

# Verify CP2K is available
echo "CP2K executable: $(which )"
 --version | head -3
echo

# Create output directory if needed
mkdir -p "$(dirname water_geo_opt_demo.out)"

# Run CP2K
echo "Starting CP2K calculation..."
echo "Input file: water_geo_opt_demo.inp"
echo "Output file: water_geo_opt_demo.out"
echo "Command:  -np $SLURM_NTASKS  -i water_geo_opt_demo.inp -o water_geo_opt_demo.out"
echo

 -np $SLURM_NTASKS  -i water_geo_opt_demo.inp -o water_geo_opt_demo.out

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
echo "Input file: water_geo_opt_demo.inp"
echo "Output file: water_geo_opt_demo.out"
echo "Runtime: $SECONDS seconds"

# Check if output file was created and has content
if [ -f "water_geo_opt_demo.out" ] && [ -s "water_geo_opt_demo.out" ]; then
    echo "Output file created successfully ($(wc -l < water_geo_opt_demo.out) lines)"
    
    # Check for completion markers
    if grep -q "PROGRAM ENDED AT" "water_geo_opt_demo.out"; then
        echo "CP2K calculation completed normally"
    elif grep -q "ABORT" "water_geo_opt_demo.out"; then
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
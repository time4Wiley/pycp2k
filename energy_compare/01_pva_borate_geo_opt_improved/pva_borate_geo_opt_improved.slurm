#!/bin/bash
#SBATCH --job-name=pva_borate_geo_opt_improved
#SBATCH --partition=xhacnormalc
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=8
#SBATCH --cpus-per-task=1
#SBATCH --time=08:00:00
#SBATCH --output=pva_borate_geo_opt_improved.out
#SBATCH --error=pva_borate_geo_opt_improved.err

# Load modules
module purge
module load intel/2021.4.0
module load intelmpi/2021.4.0
module load cp2k/2023.1

# Set environment variables
export OMP_NUM_THREADS=1
export I_MPI_PIN_DOMAIN=omp
export I_MPI_FABRICS=shm:ofi
export I_MPI_OFI_PROVIDER=verbs
export PMI_LIBRARY_PATH=/opt/ohpc/pub/mpi/libfabric/1.15.1/lib
export I_MPI_PMI_LIBRARY=${PMI_LIBRARY_PATH}/libpmi2.so

# Check CP2K availability
if ! command -v cp2k.popt &> /dev/null; then
    echo "ERROR: cp2k.popt not found in PATH"
    exit 1
fi

echo "Starting pva_borate_geo_opt improved geometry optimization"
echo "Job ID: $SLURM_JOB_ID"
echo "Node: $SLURM_NODELIST"
echo "Working directory: $PWD"
echo "Time: $(date)"

# Run CP2K
mpirun -n $SLURM_NTASKS cp2k.popt -i pva_borate_geo_opt_improved.inp -o pva_borate_geo_opt_improved.out

# Check if job completed successfully
if [ $? -eq 0 ]; then
    echo "Job completed successfully at $(date)"
    echo "Output file size: $(ls -lh pva_borate_geo_opt_improved.out | awk '{print $5}')"
else
    echo "Job failed with exit code $? at $(date)"
fi

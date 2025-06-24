#!/bin/bash
#SBATCH --job-name=cba_borate
#SBATCH --partition=xhacnormalc
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=4
#SBATCH --cpus-per-task=1
#SBATCH --time=2:00:00
#SBATCH --output=cba_borate_%j.out
#SBATCH --error=cba_borate_%j.err

# Hardened CP2K 2023.1 + Intel MPI configuration
module purge
module load cp2k-2023.1-intelmpi_2021

# Essential PMI library for Intel MPI + Slurm compatibility
export I_MPI_PMI_LIBRARY=/opt/gridview/slurm/lib/libpmi.so

# Change to job directory
cd $SLURM_SUBMIT_DIR

# Run CP2K with proven configuration
echo "Starting CP2K calculation: cba_borate"
echo "Input file: bond_energy.inp"
echo "Working directory: $(pwd)"
echo "Number of MPI processes: $SLURM_NTASKS"

srun --mpi=pmi2 cp2k.popt -i bond_energy.inp -o cba_borate.out

echo "CP2K calculation completed"

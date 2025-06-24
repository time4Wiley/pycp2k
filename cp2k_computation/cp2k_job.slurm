#!/bin/bash
#SBATCH -J cp2k_easy
#SBATCH -A your_account
#SBATCH -p compute                 # queue / partition
#SBATCH -N 1                       # nodes
#SBATCH --ntasks-per-node=32       # MPI ranks
#SBATCH --cpus-per-task=4          # OpenMP threads (total 128 cores)
#SBATCH --time=02:00:00
#SBATCH --mem=0                    # use all node memory
#SBATCH -o cp2k_%j.out
#SBATCH -e cp2k_%j.err

module purge
module load apps/cp2k/2024.1/intel2021

export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK
export CP2K_DATA_DIR=/public/home/your_user/cp2k-2024.1/data

# --- Task 1: boronate-diol complex ---
srun cp2k.psmp -in boc_complex.inp > boc.log

# --- Task 2: slab + polymer pentamer ---
# If your cluster provides a GPU build, uncomment the next two lines
# module load cuda/11.8
# srun cp2k.popt -in slab_pentamer.inp > slab.log

# CPU-only fallback
srun cp2k.psmp -in slab_pentamer.inp > slab.log 
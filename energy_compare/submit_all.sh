#!/bin/bash

echo "=== Submitting Energy Comparison Workflow ==="
echo "Using Intel MPI + CP2K 2024.1 toolchain"

echo ""
echo "Submitting PVA-Borate calculation..."
cd 01_pva_borate
PVA_JOB=$(sbatch job.slurm | awk '{print $4}')
echo "Job ID: $PVA_JOB"
cd ..

echo ""
echo "Submitting CBA-Borate calculation..."
cd 02_cba_borate  
CBA_JOB=$(sbatch job.slurm | awk '{print $4}')
echo "Job ID: $CBA_JOB"
cd ..

echo ""
echo "=== Summary ==="
echo "PVA-Borate job: $PVA_JOB"
echo "CBA-Borate job: $CBA_JOB"
echo ""
echo "Monitor with: squeue -u \$USER"
echo "Check results: tail -f */bond_energy.out" 
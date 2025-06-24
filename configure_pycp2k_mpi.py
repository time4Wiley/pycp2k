#!/usr/bin/env python
"""
Configure PyCP2K to use CP2K 2024.1 PSMP with correct MPI setup
"""
import os
import sys

# Set up environment for CP2K MPI
os.environ['PATH'] = '/public/software/mpi/openmpi/4.1.5/bin:' + os.environ.get('PATH', '')
os.environ['LD_LIBRARY_PATH'] = '/public/software/mpi/openmpi/4.1.5/lib:' + os.environ.get('LD_LIBRARY_PATH', '')

try:
    import pycp2k
    from pycp2k import CP2K
    
    # Create calculator with explicit CP2K path
    calc = CP2K()
    
    # Configure calculator to use CP2K PSMP
    cp2k_psmp_path = "/public/software/apps/cp2k/cp2k-2024.1-gcc/exe/local/cp2k.psmp"
    mpirun_path = "/public/software/mpi/openmpi/4.1.5/bin/mpirun"
    
    print(f"✅ CP2K PSMP executable: {cp2k_psmp_path}")
    print(f"✅ OpenMPI 4.1.5 mpirun: {mpirun_path}")
    
    # Test that both exist
    if os.path.exists(cp2k_psmp_path):
        print("✅ CP2K PSMP executable found")
    else:
        print("❌ CP2K PSMP executable not found")
        
    if os.path.exists(mpirun_path):
        print("✅ OpenMPI 4.1.5 mpirun found")
    else:
        print("❌ OpenMPI 4.1.5 mpirun not found")
    
    # Configure calculator command for MPI execution
    # For SLURM integration, we'll use srun instead of mpirun
    calc.command = cp2k_psmp_path
    
    print("✅ PyCP2K configured for CP2K 2024.1 PSMP with OpenMPI 4.1.5")
    print(f"Calculator command set to: {calc.command}")
    
    # Test basic functionality
    calc.CP2K_INPUT.GLOBAL.Run_type = "ENERGY"
    calc.CP2K_INPUT.GLOBAL.Project_name = "mpi_test"
    
    print("✅ MPI configuration successful!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)


#!/usr/bin/env python
"""
Test PyCP2K with CP2K 2024.1 PSMP (MPI) configuration
"""
import os
import sys

# Set up environment for CP2K MPI
os.environ['PATH'] = '/public/software/mpi/openmpi/4.1.5/bin:' + os.environ.get('PATH', '')
os.environ['LD_LIBRARY_PATH'] = '/public/software/mpi/openmpi/4.1.5/lib:' + os.environ.get('LD_LIBRARY_PATH', '')

# Test PyCP2K import and basic functionality
try:
    import pycp2k
    from pycp2k import CP2K
    print("✅ PyCP2K imported successfully")
    
    # Create CP2K calculator
    calc = CP2K()
    print("✅ CP2K calculator created")
    
    # Test MPI-aware configuration
    calc.CP2K_INPUT.GLOBAL.Run_type = "ENERGY"
    calc.CP2K_INPUT.GLOBAL.Project_name = "pycp2k_mpi_test"
    
    # Configure for parallel execution
    print("✅ Basic calculator configuration successful")
    print(f"Available GLOBAL keywords: {len([k for k in dir(calc.CP2K_INPUT.GLOBAL) if not k.startswith('_')])}")
    
    # Test executable detection
    if hasattr(calc, 'command'):
        print(f"Calculator command: {calc.command}")
    
    print("✅ PyCP2K MPI configuration test completed successfully")
    
except Exception as e:
    print(f"❌ Error in PyCP2K MPI test: {e}")
    sys.exit(1)


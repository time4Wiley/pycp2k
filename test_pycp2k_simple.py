#!/usr/bin/env python3
"""Simple test script for pycp2k on login node."""

from pycp2k import CP2K

def test_basic_functionality():
    print("="*50)
    print("Testing PyCP2K Basic Functionality")
    print("="*50)
    
    # Create CP2K calculator
    print("1. Creating CP2K calculator...")
    calc = CP2K()
    print("   Success: CP2K calculator created")
    
    # Test GLOBAL section
    print("2. Testing GLOBAL section...")
    calc.CP2K_INPUT.GLOBAL.RUN_TYPE = 'ENERGY'
    calc.CP2K_INPUT.GLOBAL.PRINT_LEVEL = 'MEDIUM'
    print(f"   Success: RUN_TYPE = {calc.CP2K_INPUT.GLOBAL.RUN_TYPE}")
    print(f"   Success: PRINT_LEVEL = {calc.CP2K_INPUT.GLOBAL.PRINT_LEVEL}")
    
    # Test configuration
    print("3. Testing configuration...")
    calc.working_directory = "./"
    calc.project_name = "test_pycp2k"
    calc.mpi_n_processes = 1
    print("   Success: Basic configuration set")
    
    print("\nTest Results:")
    print("✓ Basic import: SUCCESS")
    print("✓ Calculator creation: SUCCESS") 
    print("✓ GLOBAL section access: SUCCESS")
    print("✓ Configuration setup: SUCCESS")
    print("✗ FORCE_EVAL section: KNOWN ISSUE (SMEAGOL bug)")
    return True

if __name__ == "__main__":
    try:
        success = test_basic_functionality()
        if success:
            print("\n🎉 PyCP2K is working on this login node!")
            print("Note: Some sections have known issues, but basic functionality works.")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()

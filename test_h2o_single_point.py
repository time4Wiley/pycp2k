#!/usr/bin/env python3
"""
Test script for cp2k_slurm package: H2O single point energy calculation
"""

import sys
import os
import time
from pathlib import Path

# Add cp2k_slurm to path
sys.path.insert(0, str(Path(__file__).parent / "cp2k_slurm"))

from pycp2k import CP2K
from cp2k_slurm.job_manager import JobManager
from cp2k_slurm.profiles import ResourceProfile

def create_h2o_single_point():
    """Create a simple H2O single point energy calculation"""
    
    # Create CP2K calculator object
    calc = CP2K()
    calc.working_directory = "./"
    calc.project_name = "h2o_single_point"
    
    # Get input tree shortcuts
    CP2K_INPUT = calc.CP2K_INPUT
    GLOBAL = CP2K_INPUT.GLOBAL
    FORCE_EVAL = CP2K_INPUT.FORCE_EVAL_add()
    SUBSYS = FORCE_EVAL.SUBSYS
    DFT = FORCE_EVAL.DFT
    SCF = DFT.SCF
    
    # Global settings
    GLOBAL.Project_name = "h2o_single_point"
    GLOBAL.Run_type = "ENERGY"
    GLOBAL.Print_level = "MEDIUM"
    
    # Force evaluation
    FORCE_EVAL.Method = "Quickstep"
    FORCE_EVAL.PRINT.FORCES.Section_parameters = "ON"
    
    # DFT settings
    DFT.Basis_set_file_name = "BASIS_MOLOPT"
    DFT.Potential_file_name = "GTH_POTENTIALS"
    DFT.Charge = 0
    DFT.Multiplicity = 1
    
    # XC functional
    DFT.XC.XC_FUNCTIONAL.Section_parameters = "PBE"
    
    # SCF settings
    SCF.Scf_guess = "ATOMIC"
    SCF.Eps_scf = 1.0E-6
    SCF.Max_scf = 300
    SCF.Added_mos = 500
    SCF.DIAGONALIZATION.Section_parameters = "ON"
    SCF.DIAGONALIZATION.Algorithm = "STANDARD"
    SCF.MIXING.Section_parameters = True
    SCF.MIXING.Method = "BROYDEN_MIXING"
    SCF.MIXING.Alpha = 0.4
    SCF.MIXING.Nbroyden = 8
    
    # Basis sets and pseudopotentials
    for element, basis, potential in [
        ("O", "DZVP-MOLOPT-SR-GTH", "GTH-PBE-q6"),
        ("H", "DZVP-MOLOPT-SR-GTH", "GTH-PBE-q1")
    ]:
        kind = SUBSYS.KIND_add(element)
        kind.Basis_set = basis
        kind.Potential = potential
    
    # Water molecule coordinates (optimized geometry)
    coords = [
        ("O", 0.000000, 0.000000, 0.000000),
        ("H", 0.757000, 0.586000, 0.000000),
        ("H", -0.757000, 0.586000, 0.000000)
    ]
    
    # Add coordinates properly - each line as a separate entry
    coord_section = SUBSYS.COORD
    for atom, x, y, z in coords:
        coord_section.Default_keyword.append(f"{atom} {x:12.6f} {y:12.6f} {z:12.6f}")
    
    # Cell (gas phase - large box)
    cell = SUBSYS.CELL
    cell.A = "20.0 0.0 0.0"
    cell.B = "0.0 20.0 0.0" 
    cell.C = "0.0 0.0 20.0"
    cell.Periodic = "NONE"
    
    return calc

def main():
    """Main function to submit and monitor H2O job"""
    
    print("=== CP2K-SLURM H2O Single Point Energy Test ===\n")
    
    # Create work directory
    work_dir = Path("h2o_test_work")
    work_dir.mkdir(exist_ok=True)
    
    # Initialize job manager
    print("1. Initializing JobManager...")
    job_manager = JobManager(work_dir=work_dir)
    
    # Create CP2K input
    print("2. Creating H2O single point energy input...")
    calc = create_h2o_single_point()
    
    # Use 'quick' profile for fast testing
    print("3. Submitting job with 'quick' profile...")
    print("   Profile: 1 node, 4 tasks, 1 hour, 8GB memory")
    
    # Write the input file first
    calc.write_input_file()
    input_file = Path(calc.working_directory) / f"{calc.project_name}.inp"
    
    job_id = job_manager.submit(
        input_obj=str(input_file),
        profile="quick",
        job_name="h2o_single_point_test"
    )
    
    if job_id:
        print(f"   ✓ Job submitted successfully! Job ID: {job_id}")
        print(f"   ✓ Work directory: {work_dir.absolute()}")
        
        # Monitor job status
        print("\n4. Monitoring job status...")
        
        # Define state change callbacks
        def on_running(status):
            print(f"   ✓ Job is running on: {status.nodes or 'unknown nodes'}")
        
        def on_completed(status):
            print(f"   ✓ Job completed! Runtime: {status.runtime or 'unknown'}")
            
        def on_failed(status):
            print(f"   ✗ Job failed! Exit code: {status.exit_code}")
        
        callbacks = {
            'RUNNING': on_running,
            'COMPLETED': on_completed, 
            'FAILED': on_failed
        }
        
        # Monitor with 10-second intervals
        print("   Monitoring every 10 seconds (press Ctrl+C to stop monitoring)...")
        try:
            final_status = job_manager.wait(
                job_id, 
                poll_interval=10,
                callbacks=callbacks,
                timeout=3600  # 1 hour timeout
            )
            
            print(f"\n5. Final job status: {final_status}")
            
            # Check results if completed successfully
            if final_status and final_status.state == 'COMPLETED':
                print("\n6. Job completed successfully!")
                
                # Look for output files
                output_file = work_dir / "h2o_single_point.out"
                if output_file.exists():
                    print(f"   ✓ Output file: {output_file}")
                    
                    # Try to extract energy from output
                    try:
                        with open(output_file, 'r') as f:
                            content = f.read()
                            
                        # Look for final energy
                        for line in content.split('\n'):
                            if 'ENERGY| Total FORCE_EVAL' in line:
                                energy = line.split()[-1]
                                print(f"   ✓ Total Energy: {energy} Hartree")
                                break
                        else:
                            print("   ? Energy not found in output (calculation may have failed)")
                            
                    except Exception as e:
                        print(f"   ! Error reading output file: {e}")
                else:
                    print("   ! Output file not found")
            else:
                print(f"\n6. Job did not complete successfully: {final_status}")
                
        except KeyboardInterrupt:
            print("\n   Monitoring interrupted by user")
            print(f"   Job {job_id} is still running - you can check status with:")
            print(f"   squeue -j {job_id}")
            
    else:
        print("   ✗ Job submission failed!")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 
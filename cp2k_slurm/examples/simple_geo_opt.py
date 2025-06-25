#!/usr/bin/env python3
"""
Simple geometry optimization example using cp2k_slurm.

This example demonstrates how to:
1. Create a CP2K input for geometry optimization
2. Submit the job using cp2k_slurm
3. Monitor job completion
"""

import sys
from pathlib import Path

# Add parent directory to path to import cp2k_slurm
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from cp2k_slurm import JobManager, ResourceProfile

def create_water_geo_opt_input():
    """Create a simple water geometry optimization input."""
    
    cp2k_input = """
&GLOBAL
  PROJECT water_geo_opt
  RUN_TYPE GEO_OPT
  PRINT_LEVEL MEDIUM
&END GLOBAL

&FORCE_EVAL
  METHOD Quickstep
  &DFT
    BASIS_SET_FILE_NAME BASIS_MOLOPT
    POTENTIAL_FILE_NAME GTH_POTENTIALS
    &MGRID
      CUTOFF 400
      REL_CUTOFF 60
    &END MGRID
    &QS
      EPS_DEFAULT 1.0E-12
    &END QS
    &SCF
      SCF_GUESS ATOMIC
      EPS_SCF 1.0E-6
      MAX_SCF 100
      &OT
        MINIMIZER DIIS
        PRECONDITIONER FULL_SINGLE_INVERSE
      &END OT
    &END SCF
    &XC
      &XC_FUNCTIONAL PBE
      &END XC_FUNCTIONAL
    &END XC
  &END DFT
  &SUBSYS
    &CELL
      ABC 10.0 10.0 10.0
      PERIODIC NONE
    &END CELL
    &COORD
      O   0.000000    0.000000    0.119262
      H   0.000000    0.763239   -0.477047
      H   0.000000   -0.763239   -0.477047
    &END COORD
    &KIND H
      BASIS_SET DZVP-MOLOPT-GTH
      POTENTIAL GTH-PBE-q1
    &END KIND
    &KIND O
      BASIS_SET DZVP-MOLOPT-GTH
      POTENTIAL GTH-PBE-q6
    &END KIND
  &END SUBSYS
&END FORCE_EVAL

&MOTION
  &GEO_OPT
    TYPE MINIMIZATION
    OPTIMIZER BFGS
    MAX_ITER 200
    MAX_DR 3.0E-03
    MAX_FORCE 4.5E-04
    RMS_DR 1.5E-03
    RMS_FORCE 3.0E-04
  &END GEO_OPT
&END MOTION
"""
    
    return cp2k_input


def main():
    """Main example function."""
    print("CP2K-SLURM Simple Geometry Optimization Example")
    print("=" * 50)
    
    # Create job manager
    work_dir = Path("./cp2k_example_jobs")
    manager = JobManager(work_dir=work_dir)
    
    print(f"Working directory: {work_dir.absolute()}")
    
    # Create CP2K input
    input_content = create_water_geo_opt_input()
    
    # Show available profiles
    print("\nAvailable resource profiles:")
    from cp2k_slurm.profiles import list_profiles
    list_profiles()
    
    # Option 1: Submit with built-in profile
    print("\n1. Testing job submission with 'quick' profile...")
    print("   (This will show how the package works, but may fail without SLURM access)")
    
    try:
        job_id = manager.submit(
            input_obj=input_content,
            profile="quick",
            job_name="water_geo_opt_demo"
        )
        print(f"✓ Job submitted with ID: {job_id}")
        
        # Show what files were created
        print(f"\nFiles created in {work_dir}:")
        for file in work_dir.glob("*"):
            print(f"  - {file.name}")
        
        return 0
        
    except Exception as e:
        print(f"✗ Expected error (SLURM not available or no permissions): {e}")
        
        # Show what files would be created
        print(f"\nExample files that would be created in {work_dir}:")
        print("  - water_geo_opt_demo.inp  (CP2K input file)")
        print("  - water_geo_opt_demo.slurm  (SLURM batch script)")
        
        # Show example SLURM script content
        print("\nExample SLURM script content:")
        print("-" * 30)
        from cp2k_slurm.profiles import get_profile
        from cp2k_slurm.templates import render_slurm_script
        
        profile = get_profile("quick")
        context = {
            'job_name': 'water_geo_opt_demo',
            'input_file': 'water_geo_opt_demo.inp',
            'output_file': 'water_geo_opt_demo.out',
            'cp2k_executable': 'cp2k.popt',
            'profile': profile,
            **profile.to_sbatch_dict()
        }
        
        script_content = render_slurm_script(context)
        print(script_content[:500] + "..." if len(script_content) > 500 else script_content)
        
        return 0
    
    return 0


if __name__ == "__main__":
    sys.exit(main()) 
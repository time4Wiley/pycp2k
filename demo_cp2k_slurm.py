#!/usr/bin/env python3
"""
Demo script for cp2k_slurm package.

Shows basic functionality without actually submitting jobs.
"""

import tempfile
from pathlib import Path

# Import the cp2k_slurm package
from cp2k_slurm import JobManager, ResourceProfile, get_builtin_profiles

def main():
    print("CP2K-SLURM Integration Package Demo")
    print("=" * 40)
    
    # Show available profiles
    print("\n1. Available Resource Profiles:")
    profiles = get_builtin_profiles()
    for name, profile in profiles.items():
        print(f"   {name:15} | {profile.nodes}n × {profile.ntasks_per_node}t × {profile.cpus_per_task}c | {profile.time}")
    
    # Create a job manager
    print("\n2. Creating JobManager:")
    with tempfile.TemporaryDirectory() as temp_dir:
        manager = JobManager(work_dir=temp_dir)
        print(f"   Work directory: {manager.work_dir}")
        
        # Create a simple CP2K input
        print("\n3. Creating CP2K input file:")
        cp2k_input = """
&GLOBAL
  PROJECT_NAME water_demo
  RUN_TYPE ENERGY
&END GLOBAL

&FORCE_EVAL
  METHOD Quickstep
  &DFT
    BASIS_SET_FILE_NAME BASIS_MOLOPT
    POTENTIAL_FILE_NAME GTH_POTENTIALS
    &SCF
      EPS_SCF 1.0E-6
      MAX_SCF 50
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
      O    0.000000    0.000000    0.000000
      H    0.000000    0.000000    1.000000
      H    0.942809    0.000000   -0.333333
    &END COORD
    &KIND O
      BASIS_SET DZVP-MOLOPT-SR-GTH
      POTENTIAL GTH-PBE-q6
    &END KIND
    &KIND H
      BASIS_SET DZVP-MOLOPT-SR-GTH
      POTENTIAL GTH-PBE-q1
    &END KIND
  &END SUBSYS
&END FORCE_EVAL
"""
        
        input_file = Path(temp_dir) / "water_demo.inp"
        input_file.write_text(cp2k_input.strip())
        print(f"   Input file: {input_file.name}")
        
        # Generate SLURM script (without submitting)
        print("\n4. Generating SLURM batch script:")
        from cp2k_slurm.profiles import get_profile
        profile = get_profile("short")
        
        script_path = manager._create_batch_script(
            profile, input_file, "water_demo.out", "water_demo", None
        )
        
        print(f"   Script generated: {script_path.name}")
        print(f"   Script size: {script_path.stat().st_size} bytes")
        
        # Show part of the generated script
        print("\n5. Generated SLURM script (first 15 lines):")
        with open(script_path, 'r') as f:
            lines = f.readlines()
            for i, line in enumerate(lines[:15]):
                print(f"   {i+1:2d}: {line.rstrip()}")
        
        print(f"\n   ... (total {len(lines)} lines)")
        
        # Show what would happen if we submitted
        print("\n6. Job Submission (DRY RUN):")
        print(f"   Would submit: {input_file.name}")
        print(f"   Using profile: short ({profile.nodes}n × {profile.ntasks_per_node}t)")
        print(f"   Time limit: {profile.time}")
        print(f"   Memory: {getattr(profile, 'mem_per_cpu', 'Default')}")
        print(f"   Command: sbatch {script_path.name}")
        
        # Show custom profile example
        print("\n7. Custom Profile Example:")
        custom_profile = ResourceProfile(
            nodes=2,
            ntasks_per_node=16,
            cpus_per_task=1,
            time="12:00:00",
            memory="32G",
            partition="compute"
        )
        
        print(f"   Custom: {custom_profile.nodes}n × {custom_profile.ntasks_per_node}t × {custom_profile.cpus_per_task}c")
        print(f"   Total MPI tasks: {custom_profile.total_mpi_tasks}")
        print(f"   Total CPU cores: {custom_profile.total_cores}")
    
    print("\n" + "=" * 40)
    print("Demo completed successfully!")
    print("\nTo actually submit jobs:")
    print("  job_id = manager.submit('input.inp', profile='short')")
    print("  status = manager.wait(job_id)")
    print("\nOr use the CLI:")
    print("  cp2k_slurm submit input.inp --profile short")

if __name__ == "__main__":
    main() 
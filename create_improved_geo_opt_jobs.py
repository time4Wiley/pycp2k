#!/usr/bin/env python3
"""
Create improved geometry optimization jobs with better SCF convergence settings.
Addresses the SCF convergence failures observed in the current jobs.
"""

import os

def create_improved_pva_input():
    """Create improved PVA-borate input with better SCF settings."""
    return """&GLOBAL
  PROJECT pva_borate_geo_opt_improved
  RUN_TYPE GEO_OPT
  PRINT_LEVEL MEDIUM
&END GLOBAL

&FORCE_EVAL
  METHOD Quickstep
  &DFT
    BASIS_SET_FILE_NAME BASIS_MOLOPT
    POTENTIAL_FILE_NAME GTH_POTENTIALS
    CHARGE 0
    MULTIPLICITY 1
    
    &QS
      METHOD GPW
      EPS_DEFAULT 1.0E-12
    &END QS
    
    &MGRID
      CUTOFF 400
      REL_CUTOFF 50
    &END MGRID
    
    &XC
      &XC_FUNCTIONAL PBE
      &END XC_FUNCTIONAL
    &END XC
    
    &SCF
      SCF_GUESS ATOMIC
      EPS_SCF 1.0E-7
      MAX_SCF 200
      ADDED_MOS 20
      &MIXING
        METHOD BROYDEN_MIXING
        ALPHA 0.2
        BETA 1.5
        NBROYDEN 8
      &END MIXING
      &OUTER_SCF
        EPS_SCF 1.0E-7
        MAX_SCF 50
      &END OUTER_SCF
      &PRINT
        &RESTART
          FILENAME =pva_borate_geo_opt_improved-RESTART.wfn
        &END RESTART
      &END PRINT
    &END SCF
    
    &KPOINTS
      SCHEME MONKHORST-PACK 1 1 1
    &END KPOINTS
    
    &POISSON
      PERIODIC NONE
      PSOLVER MT
    &END POISSON
  &END DFT
  
  &SUBSYS
    &CELL
      ABC 20.0 20.0 20.0
      PERIODIC NONE
    &END CELL
    
    &COORD
      O    0.000000    0.000000    0.000000
      O    1.430000    0.000000    0.000000  
      C   -1.200000    0.000000    0.000000
      C    2.630000    0.000000    0.000000
      H   -1.600000    1.020000    0.000000
      H   -1.600000   -0.510000    0.883000
      H   -1.600000   -0.510000   -0.883000
      H    3.030000    1.020000    0.000000
      H    3.030000   -0.510000    0.883000
      H    3.030000   -0.510000   -0.883000
      B    0.715000    1.500000    0.000000
      O    0.715000    2.300000    1.200000
      O    0.715000    2.300000   -1.200000
      O    0.715000    0.100000    0.000000
      H    0.715000    3.200000    1.200000
      H    0.715000    3.200000   -1.200000
      H    0.715000   -0.800000    0.000000
    &END COORD
    
    &KIND O
      BASIS_SET DZVP-MOLOPT-SR-GTH
      POTENTIAL GTH-PBE-q6
    &END KIND
    
    &KIND C
      BASIS_SET DZVP-MOLOPT-SR-GTH
      POTENTIAL GTH-PBE-q4
    &END KIND
    
    &KIND H
      BASIS_SET DZVP-MOLOPT-SR-GTH
      POTENTIAL GTH-PBE-q1
    &END KIND
    
    &KIND B
      BASIS_SET DZVP-MOLOPT-SR-GTH
      POTENTIAL GTH-PBE-q3
    &END KIND
  &END SUBSYS
&END FORCE_EVAL

&MOTION
  &GEO_OPT
    TYPE MINIMIZATION
    OPTIMIZER BFGS
    MAX_ITER 200
    MAX_DR 1.0E-4
    MAX_FORCE 1.0E-4
    RMS_DR 1.0E-5
    RMS_FORCE 1.0E-5
    &BFGS
      TRUST_RADIUS 0.25
    &END BFGS
  &END GEO_OPT
  
  &PRINT
    &TRAJECTORY
      FORMAT XYZ
      &EACH
        GEO_OPT 1
      &END EACH
    &END TRAJECTORY
    &RESTART
      &EACH
        GEO_OPT 10
      &END EACH
    &END RESTART
  &END PRINT
&END MOTION
"""

def create_improved_cba_input():
    """Create improved CBA-borate input with better SCF settings for charged system."""
    return """&GLOBAL
  PROJECT cba_borate_geo_opt_improved
  RUN_TYPE GEO_OPT
  PRINT_LEVEL MEDIUM
&END GLOBAL

&FORCE_EVAL
  METHOD Quickstep
  &DFT
    BASIS_SET_FILE_NAME BASIS_MOLOPT
    POTENTIAL_FILE_NAME GTH_POTENTIALS
    CHARGE -2
    MULTIPLICITY 1
    
    &QS
      METHOD GPW
      EPS_DEFAULT 1.0E-12
    &END QS
    
    &MGRID
      CUTOFF 500
      REL_CUTOFF 60
    &END MGRID
    
    &XC
      &XC_FUNCTIONAL PBE
      &END XC_FUNCTIONAL
    &END XC
    
    &SCF
      SCF_GUESS ATOMIC
      EPS_SCF 1.0E-6
      MAX_SCF 300
      ADDED_MOS 30
      &MIXING
        METHOD BROYDEN_MIXING
        ALPHA 0.1
        BETA 1.0
        NBROYDEN 12
      &END MIXING
      &OUTER_SCF
        EPS_SCF 1.0E-6
        MAX_SCF 100
      &END OUTER_SCF
      &SMEAR
        METHOD FERMI_DIRAC
        ELECTRONIC_TEMPERATURE 300
      &END SMEAR
      &PRINT
        &RESTART
          FILENAME =cba_borate_geo_opt_improved-RESTART.wfn
        &END RESTART
      &END PRINT
    &END SCF
    
    &KPOINTS
      SCHEME MONKHORST-PACK 1 1 1
    &END KPOINTS
    
    &POISSON
      PERIODIC NONE
      PSOLVER MT
    &END POISSON
  &END DFT
  
  &SUBSYS
    &CELL
      ABC 25.0 25.0 25.0
      PERIODIC NONE
    &END CELL
    
    &COORD
      C    0.000000    0.000000    0.000000
      C    1.400000    0.000000    0.000000
      C    2.100000    1.200000    0.000000
      C    1.400000    2.400000    0.000000
      C    0.000000    2.400000    0.000000
      C   -0.700000    1.200000    0.000000
      C   -0.700000   -1.300000    0.000000
      O   -1.900000   -1.300000    0.000000
      O    0.000000   -2.400000    0.000000
      H    1.900000   -0.950000    0.000000
      H    3.190000    1.200000    0.000000
      H    1.900000    3.350000    0.000000
      H   -0.500000    3.350000    0.000000
      H   -1.790000    1.200000    0.000000
      B    3.000000    0.000000    2.000000
      O    4.200000    0.000000    1.200000
      O    3.000000    1.200000    2.800000
      O    3.000000   -1.200000    2.800000
      O    1.800000    0.000000    1.200000
      H    5.000000    0.000000    1.600000
      H    3.800000    1.200000    3.200000
      H    3.800000   -1.200000    3.200000
      H    1.000000    0.000000    1.600000
    &END COORD
    
    &KIND O
      BASIS_SET DZVP-MOLOPT-SR-GTH
      POTENTIAL GTH-PBE-q6
    &END KIND
    
    &KIND C
      BASIS_SET DZVP-MOLOPT-SR-GTH
      POTENTIAL GTH-PBE-q4
    &END KIND
    
    &KIND H
      BASIS_SET DZVP-MOLOPT-SR-GTH
      POTENTIAL GTH-PBE-q1
    &END KIND
    
    &KIND B
      BASIS_SET DZVP-MOLOPT-SR-GTH
      POTENTIAL GTH-PBE-q3
    &END KIND
  &END SUBSYS
&END FORCE_EVAL

&MOTION
  &GEO_OPT
    TYPE MINIMIZATION
    OPTIMIZER BFGS
    MAX_ITER 200
    MAX_DR 1.0E-4
    MAX_FORCE 1.0E-4
    RMS_DR 1.0E-5
    RMS_FORCE 1.0E-5
    &BFGS
      TRUST_RADIUS 0.15
    &END BFGS
  &END GEO_OPT
  
  &PRINT
    &TRAJECTORY
      FORMAT XYZ
      &EACH
        GEO_OPT 1
      &END EACH
    &END TRAJECTORY
    &RESTART
      &EACH
        GEO_OPT 10
      &END EACH
    &END RESTART
  &END PRINT
&END MOTION
"""

def create_improved_slurm_script(job_name, input_file):
    """Create improved SLURM script."""
    return f"""#!/bin/bash
#SBATCH --job-name={job_name}_improved
#SBATCH --partition=xhacnormalc
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=8
#SBATCH --cpus-per-task=1
#SBATCH --time=08:00:00
#SBATCH --output={job_name}_improved.out
#SBATCH --error={job_name}_improved.err

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
export I_MPI_PMI_LIBRARY=${{PMI_LIBRARY_PATH}}/libpmi2.so

# Check CP2K availability
if ! command -v cp2k.popt &> /dev/null; then
    echo "ERROR: cp2k.popt not found in PATH"
    exit 1
fi

echo "Starting {job_name} improved geometry optimization"
echo "Job ID: $SLURM_JOB_ID"
echo "Node: $SLURM_NODELIST"
echo "Working directory: $PWD"
echo "Time: $(date)"

# Run CP2K
mpirun -n $SLURM_NTASKS cp2k.popt -i {input_file} -o {job_name}_improved.out

# Check if job completed successfully
if [ $? -eq 0 ]; then
    echo "Job completed successfully at $(date)"
    echo "Output file size: $(ls -lh {job_name}_improved.out | awk '{{print $5}}')"
else
    echo "Job failed with exit code $? at $(date)"
fi
"""

def main():
    """Create improved geometry optimization jobs."""
    
    # Create directories
    pva_dir = "energy_compare/01_pva_borate_geo_opt_improved"
    cba_dir = "energy_compare/02_cba_borate_geo_opt_improved"
    
    os.makedirs(pva_dir, exist_ok=True)
    os.makedirs(cba_dir, exist_ok=True)
    
    # Create PVA-borate improved job
    with open(f"{pva_dir}/pva_borate_geo_opt_improved.inp", "w") as f:
        f.write(create_improved_pva_input())
    
    with open(f"{pva_dir}/pva_borate_geo_opt_improved.slurm", "w") as f:
        f.write(create_improved_slurm_script("pva_borate_geo_opt", "pva_borate_geo_opt_improved.inp"))
    
    # Create CBA-borate improved job
    with open(f"{cba_dir}/cba_borate_geo_opt_improved.inp", "w") as f:
        f.write(create_improved_cba_input())
    
    with open(f"{cba_dir}/cba_borate_geo_opt_improved.slurm", "w") as f:
        f.write(create_improved_slurm_script("cba_borate_geo_opt", "cba_borate_geo_opt_improved.inp"))
    
    print("✅ Created improved geometry optimization jobs:")
    print(f"   PVA-borate: {pva_dir}/")
    print(f"   CBA-borate: {cba_dir}/")
    print("\nKey improvements:")
    print("   - Non-periodic boundary conditions (PERIODIC NONE)")
    print("   - Better SCF mixing (lower alpha, more Broyden vectors)")
    print("   - More SCF cycles (200-300 max)")
    print("   - Electronic smearing for charged system")
    print("   - Higher cutoff for charged CBA system")
    print("   - Larger cell for CBA system")

if __name__ == "__main__":
    main() 
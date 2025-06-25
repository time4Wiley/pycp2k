#!/usr/bin/env python3
"""
Create frequency analysis jobs to:
1. Validate optimized geometries are true minima (no negative frequencies)
2. Calculate vibrational contributions to binding energies
3. Analyze B-O bond strengths through vibrational modes
"""

import os

def create_frequency_input(system_name, charge, coords):
    """Create frequency analysis input."""
    return f"""&GLOBAL
  PROJECT {system_name}_freq
  RUN_TYPE VIBRATIONAL_ANALYSIS
  PRINT_LEVEL MEDIUM
&END GLOBAL

&FORCE_EVAL
  METHOD Quickstep
  &DFT
    BASIS_SET_FILE_NAME BASIS_MOLOPT
    POTENTIAL_FILE_NAME GTH_POTENTIALS
    CHARGE {charge}
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
      EPS_SCF 1.0E-8
      MAX_SCF 100
      &MIXING
        METHOD BROYDEN_MIXING
        ALPHA 0.3
        BETA 1.5
        NBROYDEN 8
      &END MIXING
    &END SCF
    
    &POISSON
      PERIODIC NONE
      PSOLVER MT
    &END POISSON
  &END DFT
  
  &SUBSYS
    &CELL
      ABC 22.0 22.0 22.0
      PERIODIC NONE
    &END CELL
    
{coords}
    
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

&VIBRATIONAL_ANALYSIS
  DX 0.01
  NPROC_REP 4
  &PRINT
    &MOLDEN_VIB
      FILENAME {system_name}_vibrations.molden
    &END MOLDEN_VIB
    &PROGRAM_RUN_INFO ON
    &END PROGRAM_RUN_INFO
  &END PRINT
&END VIBRATIONAL_ANALYSIS
"""

def create_freq_slurm_script(job_name):
    """Create SLURM script for frequency analysis."""
    return f"""#!/bin/bash
#SBATCH --job-name={job_name}_freq
#SBATCH --partition=xhacnormalc
#SBATCH --nodes=1
#SBATCH --ntasks=8
#SBATCH --time=03:00:00
#SBATCH --output={job_name}_freq.out
#SBATCH --error={job_name}_freq.err

# Load CP2K module
module load cp2k-2023.1-intelmpi_2021

# Essential PMI library
export I_MPI_PMI_LIBRARY=/opt/gridview/slurm/lib/libpmi.so
export OMP_NUM_THREADS=1

echo "Starting {job_name} frequency analysis"
echo "Job ID: $SLURM_JOB_ID"
echo "Start time: $(date)"

# Run CP2K
srun --mpi=pmi2 cp2k.popt -i {job_name}_freq.inp -o {job_name}_freq.out

if [ $? -eq 0 ]; then
    echo "✅ {job_name} frequency analysis completed at $(date)"
    echo "Number of negative frequencies:"
    grep -c "VIB|Frequency.*-" {job_name}_freq.out || echo "0"
    echo "Lowest frequency:"
    grep "VIB|Frequency" {job_name}_freq.out | head -1
else
    echo "❌ {job_name} frequency analysis failed at $(date)"
fi
"""

def main():
    """Create frequency analysis jobs for optimized complexes."""
    
    print("🎵 **FREQUENCY ANALYSIS JOBS**")
    print("These will run AFTER geometry optimizations complete")
    print("=" * 50)
    
    # PVA coordinates (from optimized geometry - will need to extract later)
    pva_coords = """    &COORD
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
    &END COORD"""
    
    # CBA coordinates (from optimized geometry - will need to extract later)  
    cba_coords = """    &COORD
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
    &END COORD"""
    
    # Create frequency analysis directory
    freq_dir = "energy_compare/frequency_analysis"
    os.makedirs(freq_dir, exist_ok=True)
    
    # Create frequency jobs
    systems = [
        ("pva_borate", 0, pva_coords),
        ("cba_borate", -2, cba_coords)
    ]
    
    for system_name, charge, coords in systems:
        system_dir = f"{freq_dir}/{system_name}"
        os.makedirs(system_dir, exist_ok=True)
        
        # Write input file
        input_file = f"{system_dir}/{system_name}_freq.inp"
        with open(input_file, 'w') as f:
            f.write(create_frequency_input(system_name, charge, coords))
        
        # Write SLURM script
        slurm_file = f"{system_dir}/{system_name}_freq.slurm"
        with open(slurm_file, 'w') as f:
            f.write(create_freq_slurm_script(system_name))
        
        print(f"✅ Created {system_name} frequency analysis: {system_dir}/")
    
    print("")
    print("📝 **NOTE:** These use initial coordinates and should be updated with")
    print("optimized geometries once geometry optimizations complete!")
    print("")
    print("🎯 **PURPOSE:**")
    print("- Validate optimized geometries are true minima")
    print("- Calculate B-O vibrational frequencies") 
    print("- Analyze bond strength differences")
    print("- Zero-point energy corrections")
    print("")
    print("⏱️ **RUNTIME:** ~1-2 hours each")
    print("💰 **COST:** ~$5-8 per system")

if __name__ == "__main__":
    main() 
"""
Create frequency analysis jobs to:
1. Validate optimized geometries are true minima (no negative frequencies)
2. Calculate vibrational contributions to binding energies
3. Analyze B-O bond strengths through vibrational modes
"""

import os

def create_frequency_input(system_name, charge, coords):
    """Create frequency analysis input."""
    return f"""&GLOBAL
  PROJECT {system_name}_freq
  RUN_TYPE VIBRATIONAL_ANALYSIS
  PRINT_LEVEL MEDIUM
&END GLOBAL

&FORCE_EVAL
  METHOD Quickstep
  &DFT
    BASIS_SET_FILE_NAME BASIS_MOLOPT
    POTENTIAL_FILE_NAME GTH_POTENTIALS
    CHARGE {charge}
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
      EPS_SCF 1.0E-8
      MAX_SCF 100
      &MIXING
        METHOD BROYDEN_MIXING
        ALPHA 0.3
        BETA 1.5
        NBROYDEN 8
      &END MIXING
    &END SCF
    
    &POISSON
      PERIODIC NONE
      PSOLVER MT
    &END POISSON
  &END DFT
  
  &SUBSYS
    &CELL
      ABC 22.0 22.0 22.0
      PERIODIC NONE
    &END CELL
    
{coords}
    
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

&VIBRATIONAL_ANALYSIS
  DX 0.01
  NPROC_REP 4
  &PRINT
    &MOLDEN_VIB
      FILENAME {system_name}_vibrations.molden
    &END MOLDEN_VIB
    &PROGRAM_RUN_INFO ON
    &END PROGRAM_RUN_INFO
  &END PRINT
&END VIBRATIONAL_ANALYSIS
"""

def create_freq_slurm_script(job_name):
    """Create SLURM script for frequency analysis."""
    return f"""#!/bin/bash
#SBATCH --job-name={job_name}_freq
#SBATCH --partition=xhacnormalc
#SBATCH --nodes=1
#SBATCH --ntasks=8
#SBATCH --time=03:00:00
#SBATCH --output={job_name}_freq.out
#SBATCH --error={job_name}_freq.err

# Load CP2K module
module load cp2k-2023.1-intelmpi_2021

# Essential PMI library
export I_MPI_PMI_LIBRARY=/opt/gridview/slurm/lib/libpmi.so
export OMP_NUM_THREADS=1

echo "Starting {job_name} frequency analysis"
echo "Job ID: $SLURM_JOB_ID"
echo "Start time: $(date)"

# Run CP2K
srun --mpi=pmi2 cp2k.popt -i {job_name}_freq.inp -o {job_name}_freq.out

if [ $? -eq 0 ]; then
    echo "✅ {job_name} frequency analysis completed at $(date)"
    echo "Number of negative frequencies:"
    grep -c "VIB|Frequency.*-" {job_name}_freq.out || echo "0"
    echo "Lowest frequency:"
    grep "VIB|Frequency" {job_name}_freq.out | head -1
else
    echo "❌ {job_name} frequency analysis failed at $(date)"
fi
"""

def main():
    """Create frequency analysis jobs for optimized complexes."""
    
    print("🎵 **FREQUENCY ANALYSIS JOBS**")
    print("These will run AFTER geometry optimizations complete")
    print("=" * 50)
    
    # PVA coordinates (from optimized geometry - will need to extract later)
    pva_coords = """    &COORD
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
    &END COORD"""
    
    # CBA coordinates (from optimized geometry - will need to extract later)  
    cba_coords = """    &COORD
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
    &END COORD"""
    
    # Create frequency analysis directory
    freq_dir = "energy_compare/frequency_analysis"
    os.makedirs(freq_dir, exist_ok=True)
    
    # Create frequency jobs
    systems = [
        ("pva_borate", 0, pva_coords),
        ("cba_borate", -2, cba_coords)
    ]
    
    for system_name, charge, coords in systems:
        system_dir = f"{freq_dir}/{system_name}"
        os.makedirs(system_dir, exist_ok=True)
        
        # Write input file
        input_file = f"{system_dir}/{system_name}_freq.inp"
        with open(input_file, 'w') as f:
            f.write(create_frequency_input(system_name, charge, coords))
        
        # Write SLURM script
        slurm_file = f"{system_dir}/{system_name}_freq.slurm"
        with open(slurm_file, 'w') as f:
            f.write(create_freq_slurm_script(system_name))
        
        print(f"✅ Created {system_name} frequency analysis: {system_dir}/")
    
    print("")
    print("📝 **NOTE:** These use initial coordinates and should be updated with")
    print("optimized geometries once geometry optimizations complete!")
    print("")
    print("🎯 **PURPOSE:**")
    print("- Validate optimized geometries are true minima")
    print("- Calculate B-O vibrational frequencies") 
    print("- Analyze bond strength differences")
    print("- Zero-point energy corrections")
    print("")
    print("⏱️ **RUNTIME:** ~1-2 hours each")
    print("💰 **COST:** ~$5-8 per system")

if __name__ == "__main__":
    main() 
"""
Create frequency analysis jobs to:
1. Validate optimized geometries are true minima (no negative frequencies)
2. Calculate vibrational contributions to binding energies
3. Analyze B-O bond strengths through vibrational modes
"""

import os

def create_frequency_input(system_name, charge, coords):
    """Create frequency analysis input."""
    return f"""&GLOBAL
  PROJECT {system_name}_freq
  RUN_TYPE VIBRATIONAL_ANALYSIS
  PRINT_LEVEL MEDIUM
&END GLOBAL

&FORCE_EVAL
  METHOD Quickstep
  &DFT
    BASIS_SET_FILE_NAME BASIS_MOLOPT
    POTENTIAL_FILE_NAME GTH_POTENTIALS
    CHARGE {charge}
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
      EPS_SCF 1.0E-8
      MAX_SCF 100
      &MIXING
        METHOD BROYDEN_MIXING
        ALPHA 0.3
        BETA 1.5
        NBROYDEN 8
      &END MIXING
    &END SCF
    
    &POISSON
      PERIODIC NONE
      PSOLVER MT
    &END POISSON
  &END DFT
  
  &SUBSYS
    &CELL
      ABC 22.0 22.0 22.0
      PERIODIC NONE
    &END CELL
    
{coords}
    
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

&VIBRATIONAL_ANALYSIS
  DX 0.01
  NPROC_REP 4
  &PRINT
    &MOLDEN_VIB
      FILENAME {system_name}_vibrations.molden
    &END MOLDEN_VIB
    &PROGRAM_RUN_INFO ON
    &END PROGRAM_RUN_INFO
  &END PRINT
&END VIBRATIONAL_ANALYSIS
"""

def create_freq_slurm_script(job_name):
    """Create SLURM script for frequency analysis."""
    return f"""#!/bin/bash
#SBATCH --job-name={job_name}_freq
#SBATCH --partition=xhacnormalc
#SBATCH --nodes=1
#SBATCH --ntasks=8
#SBATCH --time=03:00:00
#SBATCH --output={job_name}_freq.out
#SBATCH --error={job_name}_freq.err

# Load CP2K module
module load cp2k-2023.1-intelmpi_2021

# Essential PMI library
export I_MPI_PMI_LIBRARY=/opt/gridview/slurm/lib/libpmi.so
export OMP_NUM_THREADS=1

echo "Starting {job_name} frequency analysis"
echo "Job ID: $SLURM_JOB_ID"
echo "Start time: $(date)"

# Run CP2K
srun --mpi=pmi2 cp2k.popt -i {job_name}_freq.inp -o {job_name}_freq.out

if [ $? -eq 0 ]; then
    echo "✅ {job_name} frequency analysis completed at $(date)"
    echo "Number of negative frequencies:"
    grep -c "VIB|Frequency.*-" {job_name}_freq.out || echo "0"
    echo "Lowest frequency:"
    grep "VIB|Frequency" {job_name}_freq.out | head -1
else
    echo "❌ {job_name} frequency analysis failed at $(date)"
fi
"""

def main():
    """Create frequency analysis jobs for optimized complexes."""
    
    print("🎵 **FREQUENCY ANALYSIS JOBS**")
    print("These will run AFTER geometry optimizations complete")
    print("=" * 50)
    
    # PVA coordinates (from optimized geometry - will need to extract later)
    pva_coords = """    &COORD
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
    &END COORD"""
    
    # CBA coordinates (from optimized geometry - will need to extract later)  
    cba_coords = """    &COORD
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
    &END COORD"""
    
    # Create frequency analysis directory
    freq_dir = "energy_compare/frequency_analysis"
    os.makedirs(freq_dir, exist_ok=True)
    
    # Create frequency jobs
    systems = [
        ("pva_borate", 0, pva_coords),
        ("cba_borate", -2, cba_coords)
    ]
    
    for system_name, charge, coords in systems:
        system_dir = f"{freq_dir}/{system_name}"
        os.makedirs(system_dir, exist_ok=True)
        
        # Write input file
        input_file = f"{system_dir}/{system_name}_freq.inp"
        with open(input_file, 'w') as f:
            f.write(create_frequency_input(system_name, charge, coords))
        
        # Write SLURM script
        slurm_file = f"{system_dir}/{system_name}_freq.slurm"
        with open(slurm_file, 'w') as f:
            f.write(create_freq_slurm_script(system_name))
        
        print(f"✅ Created {system_name} frequency analysis: {system_dir}/")
    
    print("")
    print("📝 **NOTE:** These use initial coordinates and should be updated with")
    print("optimized geometries once geometry optimizations complete!")
    print("")
    print("🎯 **PURPOSE:**")
    print("- Validate optimized geometries are true minima")
    print("- Calculate B-O vibrational frequencies") 
    print("- Analyze bond strength differences")
    print("- Zero-point energy corrections")
    print("")
    print("⏱️ **RUNTIME:** ~1-2 hours each")
    print("💰 **COST:** ~$5-8 per system")

if __name__ == "__main__":
    main() 
"""
Create frequency analysis jobs to:
1. Validate optimized geometries are true minima (no negative frequencies)
2. Calculate vibrational contributions to binding energies
3. Analyze B-O bond strengths through vibrational modes
"""

import os

def create_frequency_input(system_name, charge, coords):
    """Create frequency analysis input."""
    return f"""&GLOBAL
  PROJECT {system_name}_freq
  RUN_TYPE VIBRATIONAL_ANALYSIS
  PRINT_LEVEL MEDIUM
&END GLOBAL

&FORCE_EVAL
  METHOD Quickstep
  &DFT
    BASIS_SET_FILE_NAME BASIS_MOLOPT
    POTENTIAL_FILE_NAME GTH_POTENTIALS
    CHARGE {charge}
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
      EPS_SCF 1.0E-8
      MAX_SCF 100
      &MIXING
        METHOD BROYDEN_MIXING
        ALPHA 0.3
        BETA 1.5
        NBROYDEN 8
      &END MIXING
    &END SCF
    
    &POISSON
      PERIODIC NONE
      PSOLVER MT
    &END POISSON
  &END DFT
  
  &SUBSYS
    &CELL
      ABC 22.0 22.0 22.0
      PERIODIC NONE
    &END CELL
    
{coords}
    
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

&VIBRATIONAL_ANALYSIS
  DX 0.01
  NPROC_REP 4
  &PRINT
    &MOLDEN_VIB
      FILENAME {system_name}_vibrations.molden
    &END MOLDEN_VIB
    &PROGRAM_RUN_INFO ON
    &END PROGRAM_RUN_INFO
  &END PRINT
&END VIBRATIONAL_ANALYSIS
"""

def create_freq_slurm_script(job_name):
    """Create SLURM script for frequency analysis."""
    return f"""#!/bin/bash
#SBATCH --job-name={job_name}_freq
#SBATCH --partition=xhacnormalc
#SBATCH --nodes=1
#SBATCH --ntasks=8
#SBATCH --time=03:00:00
#SBATCH --output={job_name}_freq.out
#SBATCH --error={job_name}_freq.err

# Load CP2K module
module load cp2k-2023.1-intelmpi_2021

# Essential PMI library
export I_MPI_PMI_LIBRARY=/opt/gridview/slurm/lib/libpmi.so
export OMP_NUM_THREADS=1

echo "Starting {job_name} frequency analysis"
echo "Job ID: $SLURM_JOB_ID"
echo "Start time: $(date)"

# Run CP2K
srun --mpi=pmi2 cp2k.popt -i {job_name}_freq.inp -o {job_name}_freq.out

if [ $? -eq 0 ]; then
    echo "✅ {job_name} frequency analysis completed at $(date)"
    echo "Number of negative frequencies:"
    grep -c "VIB|Frequency.*-" {job_name}_freq.out || echo "0"
    echo "Lowest frequency:"
    grep "VIB|Frequency" {job_name}_freq.out | head -1
else
    echo "❌ {job_name} frequency analysis failed at $(date)"
fi
"""

def main():
    """Create frequency analysis jobs for optimized complexes."""
    
    print("🎵 **FREQUENCY ANALYSIS JOBS**")
    print("These will run AFTER geometry optimizations complete")
    print("=" * 50)
    
    # PVA coordinates (from optimized geometry - will need to extract later)
    pva_coords = """    &COORD
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
    &END COORD"""
    
    # CBA coordinates (from optimized geometry - will need to extract later)  
    cba_coords = """    &COORD
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
    &END COORD"""
    
    # Create frequency analysis directory
    freq_dir = "energy_compare/frequency_analysis"
    os.makedirs(freq_dir, exist_ok=True)
    
    # Create frequency jobs
    systems = [
        ("pva_borate", 0, pva_coords),
        ("cba_borate", -2, cba_coords)
    ]
    
    for system_name, charge, coords in systems:
        system_dir = f"{freq_dir}/{system_name}"
        os.makedirs(system_dir, exist_ok=True)
        
        # Write input file
        input_file = f"{system_dir}/{system_name}_freq.inp"
        with open(input_file, 'w') as f:
            f.write(create_frequency_input(system_name, charge, coords))
        
        # Write SLURM script
        slurm_file = f"{system_dir}/{system_name}_freq.slurm"
        with open(slurm_file, 'w') as f:
            f.write(create_freq_slurm_script(system_name))
        
        print(f"✅ Created {system_name} frequency analysis: {system_dir}/")
    
    print("")
    print("📝 **NOTE:** These use initial coordinates and should be updated with")
    print("optimized geometries once geometry optimizations complete!")
    print("")
    print("🎯 **PURPOSE:**")
    print("- Validate optimized geometries are true minima")
    print("- Calculate B-O vibrational frequencies") 
    print("- Analyze bond strength differences")
    print("- Zero-point energy corrections")
    print("")
    print("⏱️ **RUNTIME:** ~1-2 hours each")
    print("💰 **COST:** ~$5-8 per system")

if __name__ == "__main__":
    main() 
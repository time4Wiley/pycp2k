#!/usr/bin/env python3
"""
Create jobs to calculate individual component energies for proper binding energy analysis.
Need: isolated PVA, isolated CBA, isolated boric acid, isolated B(OH)4- for accurate binding energies.
"""

import os

def create_pva_monomer_input():
    """Ethylene glycol (PVA monomer) single point energy."""
    return """&GLOBAL
  PROJECT pva_monomer_sp
  RUN_TYPE ENERGY
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
      ABC 15.0 15.0 15.0
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
  &END SUBSYS
&END FORCE_EVAL
"""

def create_cba_monomer_input():
    """Formylbenzoate anion (CBA monomer) single point energy."""
    return """&GLOBAL
  PROJECT cba_monomer_sp
  RUN_TYPE ENERGY
  PRINT_LEVEL MEDIUM
&END GLOBAL

&FORCE_EVAL
  METHOD Quickstep
  &DFT
    BASIS_SET_FILE_NAME BASIS_MOLOPT
    POTENTIAL_FILE_NAME GTH_POTENTIALS
    CHARGE -1
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
      &MIXING
        METHOD BROYDEN_MIXING
        ALPHA 0.2
        BETA 1.0
        NBROYDEN 10
      &END MIXING
      &SMEAR
        METHOD FERMI_DIRAC
        ELECTRONIC_TEMPERATURE 300
      &END SMEAR
    &END SCF
    
    &POISSON
      PERIODIC NONE
      PSOLVER MT
    &END POISSON
  &END DFT
  
  &SUBSYS
    &CELL
      ABC 18.0 18.0 18.0
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
  &END SUBSYS
&END FORCE_EVAL
"""

def create_boric_acid_input():
    """B(OH)3 single point energy."""
    return """&GLOBAL
  PROJECT boric_acid_sp
  RUN_TYPE ENERGY
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
      ABC 12.0 12.0 12.0
      PERIODIC NONE
    &END CELL
    
    &COORD
      B    0.000000    0.000000    0.000000
      O    1.200000    0.000000    0.000000
      O   -0.600000    1.039000    0.000000
      O   -0.600000   -1.039000    0.000000
      H    2.100000    0.000000    0.000000
      H   -1.500000    1.039000    0.000000
      H   -1.500000   -1.039000    0.000000
    &END COORD
    
    &KIND O
      BASIS_SET DZVP-MOLOPT-SR-GTH
      POTENTIAL GTH-PBE-q6
    &END KIND
    
    &KIND B
      BASIS_SET DZVP-MOLOPT-SR-GTH
      POTENTIAL GTH-PBE-q3
    &END KIND
    
    &KIND H
      BASIS_SET DZVP-MOLOPT-SR-GTH
      POTENTIAL GTH-PBE-q1
    &END KIND
  &END SUBSYS
&END FORCE_EVAL
"""

def create_borate_anion_input():
    """B(OH)4- single point energy."""
    return """&GLOBAL
  PROJECT borate_anion_sp
  RUN_TYPE ENERGY
  PRINT_LEVEL MEDIUM
&END GLOBAL

&FORCE_EVAL
  METHOD Quickstep
  &DFT
    BASIS_SET_FILE_NAME BASIS_MOLOPT
    POTENTIAL_FILE_NAME GTH_POTENTIALS
    CHARGE -1
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
      MAX_SCF 150
      &MIXING
        METHOD BROYDEN_MIXING
        ALPHA 0.3
        BETA 1.0
        NBROYDEN 8
      &END MIXING
      &SMEAR
        METHOD FERMI_DIRAC
        ELECTRONIC_TEMPERATURE 300
      &END SMEAR
    &END SCF
    
    &POISSON
      PERIODIC NONE
      PSOLVER MT
    &END POISSON
  &END DFT
  
  &SUBSYS
    &CELL
      ABC 12.0 12.0 12.0
      PERIODIC NONE
    &END CELL
    
    &COORD
      B    0.000000    0.000000    0.000000
      O    1.400000    0.000000    0.000000
      O   -0.700000    1.212000    0.000000
      O   -0.700000   -1.212000    0.000000
      O    0.000000    0.000000    1.400000
      H    2.300000    0.000000    0.000000
      H   -1.600000    1.212000    0.000000
      H   -1.600000   -1.212000    0.000000
      H    0.000000    0.000000    2.300000
    &END COORD
    
    &KIND O
      BASIS_SET DZVP-MOLOPT-SR-GTH
      POTENTIAL GTH-PBE-q6
    &END KIND
    
    &KIND B
      BASIS_SET DZVP-MOLOPT-SR-GTH
      POTENTIAL GTH-PBE-q3
    &END KIND
    
    &KIND H
      BASIS_SET DZVP-MOLOPT-SR-GTH
      POTENTIAL GTH-PBE-q1
    &END KIND
  &END SUBSYS
&END FORCE_EVAL
"""

def create_component_slurm_script(job_name, input_file):
    """Create SLURM script for component energy calculations."""
    return f"""#!/bin/bash
#SBATCH --job-name={job_name}
#SBATCH --partition=xhacnormalc
#SBATCH --nodes=1
#SBATCH --ntasks=4
#SBATCH --time=01:00:00
#SBATCH --output={job_name}.out
#SBATCH --error={job_name}.err

# Load CP2K module
module load cp2k-2023.1-intelmpi_2021

# Essential PMI library
export I_MPI_PMI_LIBRARY=/opt/gridview/slurm/lib/libpmi.so
export OMP_NUM_THREADS=1

echo "Starting {job_name} single point energy calculation"
echo "Job ID: $SLURM_JOB_ID"
echo "Start time: $(date)"

# Run CP2K
srun --mpi=pmi2 cp2k.popt -i {input_file} -o {job_name}.out

if [ $? -eq 0 ]; then
    echo "✅ {job_name} completed successfully at $(date)"
    echo "Final energy:"
    grep "ENERGY|" {job_name}.out | tail -1
else
    echo "❌ {job_name} failed at $(date)"
fi
"""

def main():
    """Create all component energy calculation jobs."""
    
    # Create main directory
    comp_dir = "energy_compare/component_energies"
    os.makedirs(comp_dir, exist_ok=True)
    
    # Component calculations to create
    components = [
        ("pva_monomer", create_pva_monomer_input()),
        ("cba_monomer", create_cba_monomer_input()),
        ("boric_acid", create_boric_acid_input()),
        ("borate_anion", create_borate_anion_input())
    ]
    
    print("🧪 Creating component energy calculation jobs...")
    print("=" * 50)
    
    for comp_name, input_content in components:
        comp_subdir = f"{comp_dir}/{comp_name}"
        os.makedirs(comp_subdir, exist_ok=True)
        
        # Write input file
        input_file = f"{comp_subdir}/{comp_name}.inp"
        with open(input_file, 'w') as f:
            f.write(input_content)
        
        # Write SLURM script
        slurm_file = f"{comp_subdir}/{comp_name}.slurm"
        with open(slurm_file, 'w') as f:
            f.write(create_component_slurm_script(comp_name, f"{comp_name}.inp"))
        
        print(f"✅ Created {comp_name}: {comp_subdir}/")
    
    print("")
    print("🚀 **TO SUBMIT ALL COMPONENT JOBS:**")
    for comp_name, _ in components:
        print(f"cd {comp_dir}/{comp_name} && sbatch {comp_name}.slurm")
    
    print("")
    print("💡 **PURPOSE:**")
    print("These calculate individual component energies needed for:")
    print("- Accurate binding energy = E(complex) - E(polymer) - E(boron)")
    print("- Validation of complex formation energetics")
    print("- Comparison with experimental bond strengths")
    
    print("")
    print("⏱️ **RUNTIME:** ~10-20 minutes each (much faster than geometry opt)")
    print("💰 **COST:** ~$2-4 total for all four components")

if __name__ == "__main__":
    main() 
"""
Create jobs to calculate individual component energies for proper binding energy analysis.
Need: isolated PVA, isolated CBA, isolated boric acid, isolated B(OH)4- for accurate binding energies.
"""

import os

def create_pva_monomer_input():
    """Ethylene glycol (PVA monomer) single point energy."""
    return """&GLOBAL
  PROJECT pva_monomer_sp
  RUN_TYPE ENERGY
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
      ABC 15.0 15.0 15.0
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
  &END SUBSYS
&END FORCE_EVAL
"""

def create_cba_monomer_input():
    """Formylbenzoate anion (CBA monomer) single point energy."""
    return """&GLOBAL
  PROJECT cba_monomer_sp
  RUN_TYPE ENERGY
  PRINT_LEVEL MEDIUM
&END GLOBAL

&FORCE_EVAL
  METHOD Quickstep
  &DFT
    BASIS_SET_FILE_NAME BASIS_MOLOPT
    POTENTIAL_FILE_NAME GTH_POTENTIALS
    CHARGE -1
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
      &MIXING
        METHOD BROYDEN_MIXING
        ALPHA 0.2
        BETA 1.0
        NBROYDEN 10
      &END MIXING
      &SMEAR
        METHOD FERMI_DIRAC
        ELECTRONIC_TEMPERATURE 300
      &END SMEAR
    &END SCF
    
    &POISSON
      PERIODIC NONE
      PSOLVER MT
    &END POISSON
  &END DFT
  
  &SUBSYS
    &CELL
      ABC 18.0 18.0 18.0
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
  &END SUBSYS
&END FORCE_EVAL
"""

def create_boric_acid_input():
    """B(OH)3 single point energy."""
    return """&GLOBAL
  PROJECT boric_acid_sp
  RUN_TYPE ENERGY
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
      ABC 12.0 12.0 12.0
      PERIODIC NONE
    &END CELL
    
    &COORD
      B    0.000000    0.000000    0.000000
      O    1.200000    0.000000    0.000000
      O   -0.600000    1.039000    0.000000
      O   -0.600000   -1.039000    0.000000
      H    2.100000    0.000000    0.000000
      H   -1.500000    1.039000    0.000000
      H   -1.500000   -1.039000    0.000000
    &END COORD
    
    &KIND O
      BASIS_SET DZVP-MOLOPT-SR-GTH
      POTENTIAL GTH-PBE-q6
    &END KIND
    
    &KIND B
      BASIS_SET DZVP-MOLOPT-SR-GTH
      POTENTIAL GTH-PBE-q3
    &END KIND
    
    &KIND H
      BASIS_SET DZVP-MOLOPT-SR-GTH
      POTENTIAL GTH-PBE-q1
    &END KIND
  &END SUBSYS
&END FORCE_EVAL
"""

def create_borate_anion_input():
    """B(OH)4- single point energy."""
    return """&GLOBAL
  PROJECT borate_anion_sp
  RUN_TYPE ENERGY
  PRINT_LEVEL MEDIUM
&END GLOBAL

&FORCE_EVAL
  METHOD Quickstep
  &DFT
    BASIS_SET_FILE_NAME BASIS_MOLOPT
    POTENTIAL_FILE_NAME GTH_POTENTIALS
    CHARGE -1
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
      MAX_SCF 150
      &MIXING
        METHOD BROYDEN_MIXING
        ALPHA 0.3
        BETA 1.0
        NBROYDEN 8
      &END MIXING
      &SMEAR
        METHOD FERMI_DIRAC
        ELECTRONIC_TEMPERATURE 300
      &END SMEAR
    &END SCF
    
    &POISSON
      PERIODIC NONE
      PSOLVER MT
    &END POISSON
  &END DFT
  
  &SUBSYS
    &CELL
      ABC 12.0 12.0 12.0
      PERIODIC NONE
    &END CELL
    
    &COORD
      B    0.000000    0.000000    0.000000
      O    1.400000    0.000000    0.000000
      O   -0.700000    1.212000    0.000000
      O   -0.700000   -1.212000    0.000000
      O    0.000000    0.000000    1.400000
      H    2.300000    0.000000    0.000000
      H   -1.600000    1.212000    0.000000
      H   -1.600000   -1.212000    0.000000
      H    0.000000    0.000000    2.300000
    &END COORD
    
    &KIND O
      BASIS_SET DZVP-MOLOPT-SR-GTH
      POTENTIAL GTH-PBE-q6
    &END KIND
    
    &KIND B
      BASIS_SET DZVP-MOLOPT-SR-GTH
      POTENTIAL GTH-PBE-q3
    &END KIND
    
    &KIND H
      BASIS_SET DZVP-MOLOPT-SR-GTH
      POTENTIAL GTH-PBE-q1
    &END KIND
  &END SUBSYS
&END FORCE_EVAL
"""

def create_component_slurm_script(job_name, input_file):
    """Create SLURM script for component energy calculations."""
    return f"""#!/bin/bash
#SBATCH --job-name={job_name}
#SBATCH --partition=xhacnormalc
#SBATCH --nodes=1
#SBATCH --ntasks=4
#SBATCH --time=01:00:00
#SBATCH --output={job_name}.out
#SBATCH --error={job_name}.err

# Load CP2K module
module load cp2k-2023.1-intelmpi_2021

# Essential PMI library
export I_MPI_PMI_LIBRARY=/opt/gridview/slurm/lib/libpmi.so
export OMP_NUM_THREADS=1

echo "Starting {job_name} single point energy calculation"
echo "Job ID: $SLURM_JOB_ID"
echo "Start time: $(date)"

# Run CP2K
srun --mpi=pmi2 cp2k.popt -i {input_file} -o {job_name}.out

if [ $? -eq 0 ]; then
    echo "✅ {job_name} completed successfully at $(date)"
    echo "Final energy:"
    grep "ENERGY|" {job_name}.out | tail -1
else
    echo "❌ {job_name} failed at $(date)"
fi
"""

def main():
    """Create all component energy calculation jobs."""
    
    # Create main directory
    comp_dir = "energy_compare/component_energies"
    os.makedirs(comp_dir, exist_ok=True)
    
    # Component calculations to create
    components = [
        ("pva_monomer", create_pva_monomer_input()),
        ("cba_monomer", create_cba_monomer_input()),
        ("boric_acid", create_boric_acid_input()),
        ("borate_anion", create_borate_anion_input())
    ]
    
    print("🧪 Creating component energy calculation jobs...")
    print("=" * 50)
    
    for comp_name, input_content in components:
        comp_subdir = f"{comp_dir}/{comp_name}"
        os.makedirs(comp_subdir, exist_ok=True)
        
        # Write input file
        input_file = f"{comp_subdir}/{comp_name}.inp"
        with open(input_file, 'w') as f:
            f.write(input_content)
        
        # Write SLURM script
        slurm_file = f"{comp_subdir}/{comp_name}.slurm"
        with open(slurm_file, 'w') as f:
            f.write(create_component_slurm_script(comp_name, f"{comp_name}.inp"))
        
        print(f"✅ Created {comp_name}: {comp_subdir}/")
    
    print("")
    print("🚀 **TO SUBMIT ALL COMPONENT JOBS:**")
    for comp_name, _ in components:
        print(f"cd {comp_dir}/{comp_name} && sbatch {comp_name}.slurm")
    
    print("")
    print("💡 **PURPOSE:**")
    print("These calculate individual component energies needed for:")
    print("- Accurate binding energy = E(complex) - E(polymer) - E(boron)")
    print("- Validation of complex formation energetics")
    print("- Comparison with experimental bond strengths")
    
    print("")
    print("⏱️ **RUNTIME:** ~10-20 minutes each (much faster than geometry opt)")
    print("💰 **COST:** ~$2-4 total for all four components")

if __name__ == "__main__":
    main() 
"""
Create jobs to calculate individual component energies for proper binding energy analysis.
Need: isolated PVA, isolated CBA, isolated boric acid, isolated B(OH)4- for accurate binding energies.
"""

import os

def create_pva_monomer_input():
    """Ethylene glycol (PVA monomer) single point energy."""
    return """&GLOBAL
  PROJECT pva_monomer_sp
  RUN_TYPE ENERGY
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
      ABC 15.0 15.0 15.0
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
  &END SUBSYS
&END FORCE_EVAL
"""

def create_cba_monomer_input():
    """Formylbenzoate anion (CBA monomer) single point energy."""
    return """&GLOBAL
  PROJECT cba_monomer_sp
  RUN_TYPE ENERGY
  PRINT_LEVEL MEDIUM
&END GLOBAL

&FORCE_EVAL
  METHOD Quickstep
  &DFT
    BASIS_SET_FILE_NAME BASIS_MOLOPT
    POTENTIAL_FILE_NAME GTH_POTENTIALS
    CHARGE -1
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
      &MIXING
        METHOD BROYDEN_MIXING
        ALPHA 0.2
        BETA 1.0
        NBROYDEN 10
      &END MIXING
      &SMEAR
        METHOD FERMI_DIRAC
        ELECTRONIC_TEMPERATURE 300
      &END SMEAR
    &END SCF
    
    &POISSON
      PERIODIC NONE
      PSOLVER MT
    &END POISSON
  &END DFT
  
  &SUBSYS
    &CELL
      ABC 18.0 18.0 18.0
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
  &END SUBSYS
&END FORCE_EVAL
"""

def create_boric_acid_input():
    """B(OH)3 single point energy."""
    return """&GLOBAL
  PROJECT boric_acid_sp
  RUN_TYPE ENERGY
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
      ABC 12.0 12.0 12.0
      PERIODIC NONE
    &END CELL
    
    &COORD
      B    0.000000    0.000000    0.000000
      O    1.200000    0.000000    0.000000
      O   -0.600000    1.039000    0.000000
      O   -0.600000   -1.039000    0.000000
      H    2.100000    0.000000    0.000000
      H   -1.500000    1.039000    0.000000
      H   -1.500000   -1.039000    0.000000
    &END COORD
    
    &KIND O
      BASIS_SET DZVP-MOLOPT-SR-GTH
      POTENTIAL GTH-PBE-q6
    &END KIND
    
    &KIND B
      BASIS_SET DZVP-MOLOPT-SR-GTH
      POTENTIAL GTH-PBE-q3
    &END KIND
    
    &KIND H
      BASIS_SET DZVP-MOLOPT-SR-GTH
      POTENTIAL GTH-PBE-q1
    &END KIND
  &END SUBSYS
&END FORCE_EVAL
"""

def create_borate_anion_input():
    """B(OH)4- single point energy."""
    return """&GLOBAL
  PROJECT borate_anion_sp
  RUN_TYPE ENERGY
  PRINT_LEVEL MEDIUM
&END GLOBAL

&FORCE_EVAL
  METHOD Quickstep
  &DFT
    BASIS_SET_FILE_NAME BASIS_MOLOPT
    POTENTIAL_FILE_NAME GTH_POTENTIALS
    CHARGE -1
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
      MAX_SCF 150
      &MIXING
        METHOD BROYDEN_MIXING
        ALPHA 0.3
        BETA 1.0
        NBROYDEN 8
      &END MIXING
      &SMEAR
        METHOD FERMI_DIRAC
        ELECTRONIC_TEMPERATURE 300
      &END SMEAR
    &END SCF
    
    &POISSON
      PERIODIC NONE
      PSOLVER MT
    &END POISSON
  &END DFT
  
  &SUBSYS
    &CELL
      ABC 12.0 12.0 12.0
      PERIODIC NONE
    &END CELL
    
    &COORD
      B    0.000000    0.000000    0.000000
      O    1.400000    0.000000    0.000000
      O   -0.700000    1.212000    0.000000
      O   -0.700000   -1.212000    0.000000
      O    0.000000    0.000000    1.400000
      H    2.300000    0.000000    0.000000
      H   -1.600000    1.212000    0.000000
      H   -1.600000   -1.212000    0.000000
      H    0.000000    0.000000    2.300000
    &END COORD
    
    &KIND O
      BASIS_SET DZVP-MOLOPT-SR-GTH
      POTENTIAL GTH-PBE-q6
    &END KIND
    
    &KIND B
      BASIS_SET DZVP-MOLOPT-SR-GTH
      POTENTIAL GTH-PBE-q3
    &END KIND
    
    &KIND H
      BASIS_SET DZVP-MOLOPT-SR-GTH
      POTENTIAL GTH-PBE-q1
    &END KIND
  &END SUBSYS
&END FORCE_EVAL
"""

def create_component_slurm_script(job_name, input_file):
    """Create SLURM script for component energy calculations."""
    return f"""#!/bin/bash
#SBATCH --job-name={job_name}
#SBATCH --partition=xhacnormalc
#SBATCH --nodes=1
#SBATCH --ntasks=4
#SBATCH --time=01:00:00
#SBATCH --output={job_name}.out
#SBATCH --error={job_name}.err

# Load CP2K module
module load cp2k-2023.1-intelmpi_2021

# Essential PMI library
export I_MPI_PMI_LIBRARY=/opt/gridview/slurm/lib/libpmi.so
export OMP_NUM_THREADS=1

echo "Starting {job_name} single point energy calculation"
echo "Job ID: $SLURM_JOB_ID"
echo "Start time: $(date)"

# Run CP2K
srun --mpi=pmi2 cp2k.popt -i {input_file} -o {job_name}.out

if [ $? -eq 0 ]; then
    echo "✅ {job_name} completed successfully at $(date)"
    echo "Final energy:"
    grep "ENERGY|" {job_name}.out | tail -1
else
    echo "❌ {job_name} failed at $(date)"
fi
"""

def main():
    """Create all component energy calculation jobs."""
    
    # Create main directory
    comp_dir = "energy_compare/component_energies"
    os.makedirs(comp_dir, exist_ok=True)
    
    # Component calculations to create
    components = [
        ("pva_monomer", create_pva_monomer_input()),
        ("cba_monomer", create_cba_monomer_input()),
        ("boric_acid", create_boric_acid_input()),
        ("borate_anion", create_borate_anion_input())
    ]
    
    print("🧪 Creating component energy calculation jobs...")
    print("=" * 50)
    
    for comp_name, input_content in components:
        comp_subdir = f"{comp_dir}/{comp_name}"
        os.makedirs(comp_subdir, exist_ok=True)
        
        # Write input file
        input_file = f"{comp_subdir}/{comp_name}.inp"
        with open(input_file, 'w') as f:
            f.write(input_content)
        
        # Write SLURM script
        slurm_file = f"{comp_subdir}/{comp_name}.slurm"
        with open(slurm_file, 'w') as f:
            f.write(create_component_slurm_script(comp_name, f"{comp_name}.inp"))
        
        print(f"✅ Created {comp_name}: {comp_subdir}/")
    
    print("")
    print("🚀 **TO SUBMIT ALL COMPONENT JOBS:**")
    for comp_name, _ in components:
        print(f"cd {comp_dir}/{comp_name} && sbatch {comp_name}.slurm")
    
    print("")
    print("💡 **PURPOSE:**")
    print("These calculate individual component energies needed for:")
    print("- Accurate binding energy = E(complex) - E(polymer) - E(boron)")
    print("- Validation of complex formation energetics")
    print("- Comparison with experimental bond strengths")
    
    print("")
    print("⏱️ **RUNTIME:** ~10-20 minutes each (much faster than geometry opt)")
    print("💰 **COST:** ~$2-4 total for all four components")

if __name__ == "__main__":
    main() 
"""
Create jobs to calculate individual component energies for proper binding energy analysis.
Need: isolated PVA, isolated CBA, isolated boric acid, isolated B(OH)4- for accurate binding energies.
"""

import os

def create_pva_monomer_input():
    """Ethylene glycol (PVA monomer) single point energy."""
    return """&GLOBAL
  PROJECT pva_monomer_sp
  RUN_TYPE ENERGY
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
      ABC 15.0 15.0 15.0
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
  &END SUBSYS
&END FORCE_EVAL
"""

def create_cba_monomer_input():
    """Formylbenzoate anion (CBA monomer) single point energy."""
    return """&GLOBAL
  PROJECT cba_monomer_sp
  RUN_TYPE ENERGY
  PRINT_LEVEL MEDIUM
&END GLOBAL

&FORCE_EVAL
  METHOD Quickstep
  &DFT
    BASIS_SET_FILE_NAME BASIS_MOLOPT
    POTENTIAL_FILE_NAME GTH_POTENTIALS
    CHARGE -1
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
      &MIXING
        METHOD BROYDEN_MIXING
        ALPHA 0.2
        BETA 1.0
        NBROYDEN 10
      &END MIXING
      &SMEAR
        METHOD FERMI_DIRAC
        ELECTRONIC_TEMPERATURE 300
      &END SMEAR
    &END SCF
    
    &POISSON
      PERIODIC NONE
      PSOLVER MT
    &END POISSON
  &END DFT
  
  &SUBSYS
    &CELL
      ABC 18.0 18.0 18.0
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
  &END SUBSYS
&END FORCE_EVAL
"""

def create_boric_acid_input():
    """B(OH)3 single point energy."""
    return """&GLOBAL
  PROJECT boric_acid_sp
  RUN_TYPE ENERGY
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
      ABC 12.0 12.0 12.0
      PERIODIC NONE
    &END CELL
    
    &COORD
      B    0.000000    0.000000    0.000000
      O    1.200000    0.000000    0.000000
      O   -0.600000    1.039000    0.000000
      O   -0.600000   -1.039000    0.000000
      H    2.100000    0.000000    0.000000
      H   -1.500000    1.039000    0.000000
      H   -1.500000   -1.039000    0.000000
    &END COORD
    
    &KIND O
      BASIS_SET DZVP-MOLOPT-SR-GTH
      POTENTIAL GTH-PBE-q6
    &END KIND
    
    &KIND B
      BASIS_SET DZVP-MOLOPT-SR-GTH
      POTENTIAL GTH-PBE-q3
    &END KIND
    
    &KIND H
      BASIS_SET DZVP-MOLOPT-SR-GTH
      POTENTIAL GTH-PBE-q1
    &END KIND
  &END SUBSYS
&END FORCE_EVAL
"""

def create_borate_anion_input():
    """B(OH)4- single point energy."""
    return """&GLOBAL
  PROJECT borate_anion_sp
  RUN_TYPE ENERGY
  PRINT_LEVEL MEDIUM
&END GLOBAL

&FORCE_EVAL
  METHOD Quickstep
  &DFT
    BASIS_SET_FILE_NAME BASIS_MOLOPT
    POTENTIAL_FILE_NAME GTH_POTENTIALS
    CHARGE -1
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
      MAX_SCF 150
      &MIXING
        METHOD BROYDEN_MIXING
        ALPHA 0.3
        BETA 1.0
        NBROYDEN 8
      &END MIXING
      &SMEAR
        METHOD FERMI_DIRAC
        ELECTRONIC_TEMPERATURE 300
      &END SMEAR
    &END SCF
    
    &POISSON
      PERIODIC NONE
      PSOLVER MT
    &END POISSON
  &END DFT
  
  &SUBSYS
    &CELL
      ABC 12.0 12.0 12.0
      PERIODIC NONE
    &END CELL
    
    &COORD
      B    0.000000    0.000000    0.000000
      O    1.400000    0.000000    0.000000
      O   -0.700000    1.212000    0.000000
      O   -0.700000   -1.212000    0.000000
      O    0.000000    0.000000    1.400000
      H    2.300000    0.000000    0.000000
      H   -1.600000    1.212000    0.000000
      H   -1.600000   -1.212000    0.000000
      H    0.000000    0.000000    2.300000
    &END COORD
    
    &KIND O
      BASIS_SET DZVP-MOLOPT-SR-GTH
      POTENTIAL GTH-PBE-q6
    &END KIND
    
    &KIND B
      BASIS_SET DZVP-MOLOPT-SR-GTH
      POTENTIAL GTH-PBE-q3
    &END KIND
    
    &KIND H
      BASIS_SET DZVP-MOLOPT-SR-GTH
      POTENTIAL GTH-PBE-q1
    &END KIND
  &END SUBSYS
&END FORCE_EVAL
"""

def create_component_slurm_script(job_name, input_file):
    """Create SLURM script for component energy calculations."""
    return f"""#!/bin/bash
#SBATCH --job-name={job_name}
#SBATCH --partition=xhacnormalc
#SBATCH --nodes=1
#SBATCH --ntasks=4
#SBATCH --time=01:00:00
#SBATCH --output={job_name}.out
#SBATCH --error={job_name}.err

# Load CP2K module
module load cp2k-2023.1-intelmpi_2021

# Essential PMI library
export I_MPI_PMI_LIBRARY=/opt/gridview/slurm/lib/libpmi.so
export OMP_NUM_THREADS=1

echo "Starting {job_name} single point energy calculation"
echo "Job ID: $SLURM_JOB_ID"
echo "Start time: $(date)"

# Run CP2K
srun --mpi=pmi2 cp2k.popt -i {input_file} -o {job_name}.out

if [ $? -eq 0 ]; then
    echo "✅ {job_name} completed successfully at $(date)"
    echo "Final energy:"
    grep "ENERGY|" {job_name}.out | tail -1
else
    echo "❌ {job_name} failed at $(date)"
fi
"""

def main():
    """Create all component energy calculation jobs."""
    
    # Create main directory
    comp_dir = "energy_compare/component_energies"
    os.makedirs(comp_dir, exist_ok=True)
    
    # Component calculations to create
    components = [
        ("pva_monomer", create_pva_monomer_input()),
        ("cba_monomer", create_cba_monomer_input()),
        ("boric_acid", create_boric_acid_input()),
        ("borate_anion", create_borate_anion_input())
    ]
    
    print("🧪 Creating component energy calculation jobs...")
    print("=" * 50)
    
    for comp_name, input_content in components:
        comp_subdir = f"{comp_dir}/{comp_name}"
        os.makedirs(comp_subdir, exist_ok=True)
        
        # Write input file
        input_file = f"{comp_subdir}/{comp_name}.inp"
        with open(input_file, 'w') as f:
            f.write(input_content)
        
        # Write SLURM script
        slurm_file = f"{comp_subdir}/{comp_name}.slurm"
        with open(slurm_file, 'w') as f:
            f.write(create_component_slurm_script(comp_name, f"{comp_name}.inp"))
        
        print(f"✅ Created {comp_name}: {comp_subdir}/")
    
    print("")
    print("🚀 **TO SUBMIT ALL COMPONENT JOBS:**")
    for comp_name, _ in components:
        print(f"cd {comp_dir}/{comp_name} && sbatch {comp_name}.slurm")
    
    print("")
    print("💡 **PURPOSE:**")
    print("These calculate individual component energies needed for:")
    print("- Accurate binding energy = E(complex) - E(polymer) - E(boron)")
    print("- Validation of complex formation energetics")
    print("- Comparison with experimental bond strengths")
    
    print("")
    print("⏱️ **RUNTIME:** ~10-20 minutes each (much faster than geometry opt)")
    print("💰 **COST:** ~$2-4 total for all four components")

if __name__ == "__main__":
    main() 
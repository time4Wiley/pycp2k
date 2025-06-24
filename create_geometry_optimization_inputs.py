#!/usr/bin/env python3
"""
Create CP2K geometry optimization inputs for binding energy calculations
with real molecular coordinates from structure files.
"""

import os
import shutil

def create_pva_borate_structure():
    """Create PVA-borate complex using ethylene glycol + B(OH)3"""
    # Ethylene glycol coordinates (PVA-like diol)
    ethylene_glycol = """O       -1.39150000      -0.57960000      -0.14880000
O        1.39150000      -0.57960000       0.14880000
C       -0.69790000       0.57960000       0.29670000
C        0.69790000       0.57960000      -0.29660000
H       -1.26040000       1.46810000      -0.00400000
H       -0.65630000       0.53560000       1.38900000
H        1.25790000       1.46250000       0.02370000
H        0.66830000       0.55400000      -1.39040000
H       -1.44550000      -0.53400000      -1.11860000
H        0.87730000      -1.35460000      -0.13550000"""
    
    # B(OH)3 positioned to interact with glycol oxygens (3 Å away, above)
    boric_acid = """B        0.00000000       0.00000000       3.00000000
O       -1.20000000       0.69300000       3.60000000
O        1.20000000       0.69300000       3.60000000
O        0.00000000      -1.38600000       3.60000000
H       -1.80000000       1.03950000       4.20000000
H        1.80000000       1.03950000       4.20000000
H        0.00000000      -2.07900000       4.20000000"""
    
    return ethylene_glycol + "\n" + boric_acid

def create_cba_borate_structure():
    """Create CBA-borate complex using formylbenzoate anion + B(OH)4-"""
    # Formylbenzoate anion coordinates (CBA-like carboxylate)
    formylbenzoate = """O        3.07700000      -1.28870000       0.00050000
O        3.25990000       0.96180000      -0.00060000
C        1.08370000       0.00600000       0.00070000
C       -1.69680000       0.23240000      -0.00100000
C        0.48650000       1.26660000       0.00050000
C        0.29060000      -1.14130000       0.00000000
C       -0.90380000       1.37980000      -0.00020000
C       -1.09970000      -1.02830000      -0.00080000
C        2.55060000      -0.11320000       0.00000000
C       -3.14610000       0.35040000       0.00100000
H        1.07800000       2.17810000       0.00080000
H        0.72700000      -2.13650000       0.00000000
H       -1.35450000       2.36890000       0.00020000
H       -1.69800000      -1.93560000      -0.00100000
H       -3.55980000       1.37320000       0.00250000"""
    
    # B(OH)4- positioned to interact with carboxylate oxygens (3.5 Å away)
    borate_anion = """B        5.50000000      -0.16000000       0.00000000
O        4.80000000      -1.50000000       0.00000000
O        6.20000000      -1.50000000       0.00000000
O        4.80000000       1.18000000       0.00000000
O        6.20000000       1.18000000       0.00000000
H        4.00000000      -1.80000000       0.00000000
H        7.00000000      -1.80000000       0.00000000
H        4.00000000       1.48000000       0.00000000
H        7.00000000       1.48000000       0.00000000"""
    
    return formylbenzoate + "\n" + borate_anion

def create_cp2k_geo_opt_input(system_name, coords, charge, output_dir):
    """Create CP2K geometry optimization input file"""
    
    # Count atoms
    coord_lines = [line for line in coords.strip().split('\n') if line.strip() and not line.startswith('#')]
    natoms = len(coord_lines)
    
    # Determine unique elements for KIND sections
    elements = set()
    for line in coord_lines:
        if line.strip():
            elements.add(line.split()[0])
    
    # Create KIND sections
    kind_sections = ""
    for element in sorted(elements):
        if element == 'H':
            potential = "GTH-PBE-q1"
        elif element == 'C':
            potential = "GTH-PBE-q4"
        elif element == 'O':
            potential = "GTH-PBE-q6"
        elif element == 'B':
            potential = "GTH-PBE-q3"
        else:
            potential = f"GTH-PBE"  # fallback
            
        kind_sections += f"""    &KIND {element}
      POTENTIAL {potential}
      BASIS_SET DZVP-MOLOPT-SR-GTH
    &END KIND
"""
    
    input_content = f"""&GLOBAL
  PRINT_LEVEL MEDIUM
  PROJECT_NAME {system_name}_geo_opt
  RUN_TYPE GEO_OPT
&END GLOBAL

&MOTION
  &GEO_OPT
    OPTIMIZER BFGS
    MAX_ITER 200
    MAX_DR 0.001
    MAX_FORCE 0.0005
    RMS_DR 0.0005
    RMS_FORCE 0.0003
  &END GEO_OPT
&END MOTION

&FORCE_EVAL
  METHOD Quickstep
  &DFT
    POTENTIAL_FILE_NAME GTH_POTENTIALS
    CHARGE {charge}
    BASIS_SET_FILE_NAME BASIS_MOLOPT
    &SCF
      MAX_SCF 100
      EPS_SCF 1e-06
      SCF_GUESS ATOMIC
      &MIXING
        METHOD BROYDEN_MIXING
        ALPHA 0.4
        NBUFFER 8
      &END MIXING
    &END SCF
    &MGRID
      NGRIDS 4
      CUTOFF 400
      REL_CUTOFF 50
    &END MGRID
    &XC
      &XC_FUNCTIONAL
        &PBE
          SCALE_X 1.0
          SCALE_C 1.0
        &END PBE
      &END XC_FUNCTIONAL
    &END XC
  &END DFT
  &SUBSYS
    &CELL
      A 15.0 0.0 0.0
      B 0.0 15.0 0.0
      C 0.0 0.0 15.0
      PERIODIC NONE
    &END CELL
    &COORD
{coords}
    &END COORD
{kind_sections}  &END SUBSYS
&END FORCE_EVAL
"""
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Write input file
    input_file = os.path.join(output_dir, f"{system_name}_geo_opt.inp")
    with open(input_file, 'w') as f:
        f.write(input_content)
    
    print(f"Created geometry optimization input: {input_file}")
    return input_file

def main():
    """Generate geometry optimization inputs"""
    
    # Create directories
    pva_dir = "energy_compare/01_pva_borate_geo_opt"
    cba_dir = "energy_compare/02_cba_borate_geo_opt"
    
    # Generate PVA-borate system (neutral)
    pva_coords = create_pva_borate_structure()
    pva_input = create_cp2k_geo_opt_input("pva_borate", pva_coords, 0, pva_dir)
    
    # Generate CBA-borate system (charge -2: COO- + B(OH)4-)  
    cba_coords = create_cba_borate_structure()
    cba_input = create_cp2k_geo_opt_input("cba_borate", cba_coords, -2, cba_dir)
    
    print(f"\nGenerated geometry optimization inputs:")
    print(f"PVA-borate: {pva_input}")
    print(f"CBA-borate: {cba_input}")
    print(f"\nNext steps:")
    print(f"1. Create SLURM jobs for these geometry optimizations")
    print(f"2. Run optimizations")
    print(f"3. Use optimized geometries for energy calculations")

if __name__ == "__main__":
    main() 
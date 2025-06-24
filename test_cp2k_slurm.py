#!/usr/bin/env python3
"""
PyCP2K SLURM test with CP2K 2024.1
Auto basis set detection - NO manual copying required
"""

import os
from pycp2k import CP2K

def create_cp2k_slurm_test():
    print("=== Creating PyCP2K SLURM Test (CP2K 2024.1) ===")
    
    # Create H2O geometry
    with open('h2o.xyz', 'w') as f:
        f.write("""3
H2O molecule for SLURM test
O   0.000000   0.000000   0.000000
H   0.757000   0.586000   0.000000
H  -0.757000   0.586000   0.000000
""")
    
    # Setup CP2K calculation
    calc = CP2K()
    
    # Global settings
    calc.CP2K_INPUT.GLOBAL.Project_name = 'h2o_slurm_test'
    calc.CP2K_INPUT.GLOBAL.Run_type = 'ENERGY_FORCE'
    calc.CP2K_INPUT.GLOBAL.Print_level = 'MEDIUM'
    
    # Force evaluation
    fe = calc.CP2K_INPUT.FORCE_EVAL_add()
    fe.Method = 'Quickstep'
    
    # DFT with AUTO BASIS SETS from CP2K 2024.1
    dft = fe.DFT
    dft.Basis_set_file_name = 'BASIS_MOLOPT'      # Auto-found!
    dft.Potential_file_name = 'GTH_POTENTIALS'    # Auto-found!
    dft.Uks = False
    dft.Charge = 0
    dft.Multiplicity = 1
    
    # XC functional
    dft.XC.XC_FUNCTIONAL.PBE.Section_parameters = 'ON'
    
    # SCF settings
    scf = dft.SCF
    scf.Scf_guess = 'ATOMIC'
    scf.Eps_scf = 1.0e-6
    scf.Max_scf = 100
    scf.Added_mos = 20
    
    # Subsystem
    subsys = fe.SUBSYS
    subsys.TOPOLOGY.Coord_file_name = 'h2o.xyz'
    subsys.TOPOLOGY.Coordinate = 'xyz'
    
    # Cell (isolated molecule)
    cell = subsys.CELL
    cell.A = '12.0 0.0 0.0'
    cell.B = '0.0 12.0 0.0'
    cell.C = '0.0 0.0 12.0'
    cell.Periodic = 'NONE'
    
    # Atomic kinds - basis sets auto-detected from CP2K_DATA_DIR
    kind_o = subsys.KIND_add('O')
    kind_o.Basis_set = 'DZVP-MOLOPT-SR-GTH'
    kind_o.Potential = 'GTH-PBE-q6'
    
    kind_h = subsys.KIND_add('H')
    kind_h.Basis_set = 'DZVP-MOLOPT-SR-GTH'
    kind_h.Potential = 'GTH-PBE-q1'
    
    # Print forces
    fe.PRINT.FORCES.Section_parameters = 'ON'
    
    # Generate CP2K input
    with open('cp2k_slurm.inp', 'w') as f:
        f.write(calc.get_input_string())
    
    print("✓ CP2K input file generated: cp2k_slurm.inp")
    print("✓ Using CP2K 2024.1 auto basis set detection")
    print("✓ NO manual basis set copying required!")
    
    # Create SLURM script
    slurm_script = """#!/bin/bash
#SBATCH --job-name=pycp2k_test
#SBATCH --partition=small
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=4
#SBATCH --time=00:10:00
#SBATCH --output=pycp2k_test_%j.out
#SBATCH --error=pycp2k_test_%j.err

echo "=== PyCP2K SLURM Test with CP2K 2024.1 ==="
echo "Job ID: $SLURM_JOB_ID"
echo "Node: $SLURM_NODELIST"
echo "Tasks: $SLURM_NTASKS"
echo "Date: $(date)"

# Load CP2K 2024.1 - NO GLIBC ISSUES!
module load cp2k-2024.1-gcc-930-nopython
module load anaconda3/2023.09

echo "CP2K_DATA_DIR: $CP2K_DATA_DIR"
echo "CP2K executable: $(which cp2k.psmp)"

# Run CP2K with MPI
echo "Starting CP2K calculation..."
mpirun -np $SLURM_NTASKS cp2k.psmp -i cp2k_slurm.inp -o cp2k_slurm.out

# Check results
if [ -f cp2k_slurm.out ]; then
    echo "=== Calculation completed ==="
    if grep -q "ENERGY| Total FORCE_EVAL" cp2k_slurm.out; then
        echo "✅ SUCCESS: Energy calculation completed!"
        grep "ENERGY| Total FORCE_EVAL" cp2k_slurm.out | tail -1
    else
        echo "⚠️ Calculation may not have finished"
        tail -20 cp2k_slurm.out
    fi
    
    echo "=== Timing Info ==="
    grep "CP2K                                 " cp2k_slurm.out || echo "No timing found"
    
    echo "=== Basis Set Confirmation ==="
    grep -i "basis.*molopt" cp2k_slurm.out | head -3 || echo "Basis set info not found"
    grep -i "potential.*gth" cp2k_slurm.out | head -3 || echo "Potential info not found"
else
    echo "❌ No output file found!"
    ls -la
fi

echo "Job completed at $(date)"
"""
    
    with open('submit_pycp2k_test.slurm', 'w') as f:
        f.write(slurm_script)
    
    print("✓ SLURM script created: submit_pycp2k_test.slurm")
    
    # Show files created
    print("\n=== Files Created ===")
    print("📄 h2o.xyz - H2O geometry")
    print("📄 cp2k_slurm.inp - CP2K input with auto basis sets")
    print("📄 submit_pycp2k_test.slurm - SLURM submission script")
    
    return True

if __name__ == '__main__':
    create_cp2k_slurm_test()

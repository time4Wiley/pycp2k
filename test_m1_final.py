#!/usr/bin/env python3

import os
import tempfile
from pycp2k import CP2K

def test_cp2k_2024_final():
    print("=== CP2K 2024 Final Test (4 cores psmp) ===")
    print(f"CP2K_DATA_DIR: {os.environ.get('CP2K_DATA_DIR', 'NOT SET')}")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        print(f"Working directory: {tmpdir}")
        
        # Create H2O geometry file
        h2o_xyz = os.path.join(tmpdir, "h2o.xyz")
        with open(h2o_xyz, 'w') as f:
            f.write("""3
H2O molecule
O   0.000000   0.000000   0.000000
H   0.757000   0.586000   0.000000
H  -0.757000   0.586000   0.000000
""")
        
        # Set up CP2K calculation
        calc = CP2K()
        calc.working_directory = tmpdir
        
        # Global settings
        calc.CP2K_INPUT.GLOBAL.Project_name = 'h2o_test'
        calc.CP2K_INPUT.GLOBAL.Run_type = 'ENERGY_FORCE'
        calc.CP2K_INPUT.GLOBAL.Print_level = 'MEDIUM'
        
        # Force evaluation
        fe = calc.CP2K_INPUT.FORCE_EVAL_add()
        fe.Method = 'Quickstep'
        
        # DFT settings - BASIS SETS FOUND AUTOMATICALLY
        dft = fe.DFT
        dft.Basis_set_file_name = 'BASIS_MOLOPT'  # Auto-found in CP2K_DATA_DIR
        dft.Potential_file_name = 'GTH_POTENTIALS'  # Auto-found in CP2K_DATA_DIR
        dft.Uks = False
        dft.Charge = 0
        dft.Multiplicity = 1
        
        # XC functional - simple PBE
        dft.XC.XC_FUNCTIONAL.PBE.Section_parameters = 'ON'
        
        # SCF settings
        scf = dft.SCF
        scf.Scf_guess = 'ATOMIC'
        scf.Eps_scf = 1.0e-6
        scf.Max_scf = 50
        
        # Subsystem
        subsys = fe.SUBSYS
        subsys.TOPOLOGY.Coord_file_name = 'h2o.xyz'
        subsys.TOPOLOGY.Coordinate = 'xyz'
        
        # Cell (for isolated molecule)
        cell = subsys.CELL
        cell.A = '10.0 0.0 0.0'
        cell.B = '0.0 10.0 0.0' 
        cell.C = '0.0 0.0 10.0'
        cell.Periodic = 'NONE'
        
        # Define atomic kinds - basis sets auto-detected
        kind_o = subsys.KIND_add('O')
        kind_o.Basis_set = 'DZVP-MOLOPT-SR-GTH'
        kind_o.Potential = 'GTH-PBE-q6'
        
        kind_h = subsys.KIND_add('H')
        kind_h.Basis_set = 'DZVP-MOLOPT-SR-GTH'
        kind_h.Potential = 'GTH-PBE-q1'
        
        # Generate input file
        input_file = os.path.join(tmpdir, 'cp2k.inp')
        calc.write_input_file(input_file)
        
        print("✓ Input file generated successfully")
        print("✓ Using automatic basis set detection from CP2K_DATA_DIR")
        print("✓ No manual basis set copying required")
        
        # Display the input for verification
        with open(input_file, 'r') as f:
            content = f.read()
            print("\n=== Generated CP2K Input ===")
            print(content[:1000] + "..." if len(content) > 1000 else content)
        
        # Run CP2K with 4 cores (psmp)
        print("\n=== Running CP2K with 4 cores (psmp) ===")
        calc.run(command='mpirun -np 4 cp2k.psmp -i cp2k.inp -o cp2k.out')
        
        # Check output
        output_file = os.path.join(tmpdir, 'cp2k.out')
        if os.path.exists(output_file):
            with open(output_file, 'r') as f:
                output = f.read()
                if 'ENERGY| Total FORCE_EVAL' in output:
                    print("✓ CP2K calculation completed successfully!")
                    
                    # Extract energy
                    for line in output.split('\n'):
                        if 'ENERGY| Total FORCE_EVAL' in line:
                            energy = line.split()[-1]
                            print(f"✓ Total energy: {energy} Hartree")
                            break
                else:
                    print("✗ CP2K calculation may have failed")
                    print("Last 20 lines of output:")
                    print('\n'.join(output.split('\n')[-20:]))
        else:
            print("✗ No output file found")

if __name__ == '__main__':
    test_cp2k_2024_final()

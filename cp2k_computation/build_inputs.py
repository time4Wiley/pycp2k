"""
build_inputs.py
Generate CP2K input files for Easy-Step 1:

  1. boc_complex.inp   – boronate + cis-diol (≈45 atoms)
  2. slab_pentamer.inp – Ti3C2(OH)2 3×1 slab + PVA-CBA pentamer (≈170 atoms)

Replace the placeholder XYZ files with accurate geometries before running:
    python build_inputs.py --complex boc_complex.xyz --slab slab_pentamer.xyz
"""

import argparse
import sys
from pathlib import Path
from ase.io import read

# Add parent directory to path to import pycp2k
sys.path.insert(0, '..')
from pycp2k import CP2K


def base_cp2k(project: str) -> CP2K:
    """Return a minimal CP2K object with PBE-D3 settings."""
    inp = CP2K()
    inp.CP2K_INPUT.GLOBAL.Project_name = project
    inp.CP2K_INPUT.GLOBAL.Run_type = "GEO_OPT"

    # Create FORCE_EVAL section
    force_eval = inp.CP2K_INPUT.FORCE_EVAL_add()
    force_eval.Method = "Quickstep"

    # Grid & files
    force_eval.DFT.MGRID.Cutoff = 400
    force_eval.DFT.MGRID.Rel_cutoff = 60
    force_eval.DFT.Basis_set_file_name = "BASIS_MOLOPT"
    force_eval.DFT.Potential_file_name = "GTH_POTENTIALS"

    # SCF & OT
    force_eval.DFT.SCF.Eps_scf = 1.0e-6
    force_eval.DFT.SCF.OT.Preconditioner = "FULL_SINGLE_INVERSE"

    # XC: PBE + D3
    force_eval.DFT.XC.XC_FUNCTIONAL.Section_parameters = "PBE"
    
    # Add D3 dispersion correction
    force_eval.DFT.XC.VDW_POTENTIAL.Potential_type = "PAIR_POTENTIAL"
    pair_pot = force_eval.DFT.XC.VDW_POTENTIAL.PAIR_POTENTIAL_add()
    pair_pot.Type = "DFTD3"
    pair_pot.Reference_functional = "PBE"

    return inp


def write_input(xyz: str, outfile: str, box=(15, 15, 15), kmesh=None):
    atoms = read(xyz)
    inp = base_cp2k(Path(outfile).stem)

    # Get the FORCE_EVAL section that was added
    force_eval = inp.CP2K_INPUT.FORCE_EVAL_list[0]

    # Cell
    cell = force_eval.SUBSYS.CELL
    cell.A = [box[0], 0, 0]
    cell.B = [0, box[1], 0] 
    cell.C = [0, 0, box[2]]

    # k-points for slab
    if kmesh:
        force_eval.DFT.KPOINTS.Scheme = f"MONKHORST-PACK {kmesh[0]} {kmesh[1]} {kmesh[2]}"

    # Coordinates
    for sym, (x, y, z) in zip(atoms.get_chemical_symbols(), atoms.positions):
        force_eval.SUBSYS.COORD.Default_keyword.append([sym, x, y, z])

    inp.write_input_file(outfile)
    print(f"Wrote {outfile}  (atoms = {len(atoms)})")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--complex", default="boc_complex.xyz",
                    help="XYZ file for boronate+diol complex")
    ap.add_argument("--slab", default="slab_pentamer.xyz",
                    help="XYZ file for slab + polymer pentamer")
    args = ap.parse_args()

    write_input(args.complex, "boc_complex.inp")               # 15 Å box, Γ-point
    write_input(args.slab, "slab_pentamer.inp",
                box=(15, 10, 25), kmesh=(3, 3, 1))             # slab cell & k-mesh


if __name__ == "__main__":
    main() 
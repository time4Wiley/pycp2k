# CP2K Computation Setup

This directory contains a complete setup for running CP2K calculations on boronate-diol complexes and slab systems.

## Files Overview

### Scripts
- `build_inputs.py` - Main script that generates CP2K input files from XYZ structures
- `convert_structures.py` - Helper script that downloads molecular structures and converts them to XYZ format
- `cp2k_job.slurm` - SLURM batch script for HPC clusters (for reference)

### Generated Input Files
- `boc_complex.inp` - CP2K input for boronate + cis-diol complex (≈52 atoms)
- `slab_pentamer.inp` - CP2K input for Ti₃C₂(OH)₂ 3×1 slab + PVA-CBA pentamer (≈70 atoms)

### Molecular Structures
- `boric_acid.xyz` - B(OH)₃ structure from COD database
- `ethylene_glycol.xyz` - Ethylene glycol (diol proxy) from PubChem
- `formylbenzoate.xyz` - 4-Formylbenzoate anion from PubChem
- `boc_complex.xyz` - Combined boronate-diol complex
- `slab_pentamer.xyz` - Combined slab + polymer system

### Raw Downloads
- `boric_acid.cif` - Original CIF file from COD
- `ethylene_glycol.sdf` - Original SDF from PubChem
- `formylbenzoate.sdf` - Original SDF from PubChem

## Usage

1. **Generate structures** (already done):
   ```bash
   python convert_structures.py
   ```

2. **Generate CP2K inputs** (already done):
   ```bash
   python build_inputs.py
   ```

3. **For custom structures**, replace the XYZ files and rerun:
   ```bash
   python build_inputs.py --complex your_complex.xyz --slab your_slab.xyz
   ```

## Computational Settings

### Both Systems
- **Method**: DFT with PBE functional + D3 dispersion correction
- **Basis sets**: BASIS_MOLOPT 
- **Pseudopotentials**: GTH_POTENTIALS
- **Cutoff**: 400 Ry (plane wave), 60 Ry (relative)
- **SCF**: Orbital transformation (OT) with FULL_SINGLE_INVERSE preconditioner

### BOC Complex (`boc_complex.inp`)
- **Cell**: 15×15×15 Å cubic box
- **k-points**: Γ-point only (molecular system)
- **Atoms**: 52 (boric acid + ethylene glycol)

### Slab System (`slab_pentamer.inp`)
- **Cell**: 15×10×25 Å 
- **k-points**: 3×3×1 Monkhorst-Pack mesh
- **Atoms**: 70 (Ti slab + surface OH + formylbenzoate)

## Dependencies

- Python 3.x
- ASE (Atomic Simulation Environment)
- PyCP2K (local version in parent directory)

## Notes

- The Ti₃C₂(OH)₂ slab is a placeholder structure. For real calculations, obtain the actual MXene structure from Materials Project (mp-997282)
- The current setup uses simplified molecular models. Real polymer chains would be much larger
- All systems are set for geometry optimization (`GEO_OPT`)
- The SLURM script is configured for a typical HPC setup (modify as needed)

## Quick Start

The input files are ready to run. On an HPC cluster with CP2K installed:

```bash
# Submit both jobs (modify cp2k_job.slurm as needed)
sbatch cp2k_job.slurm
```

For local testing (if CP2K is installed):

```bash
# Run the molecular complex
cp2k.psmp -in boc_complex.inp > boc.log

# Run the slab system  
cp2k.psmp -in slab_pentamer.inp > slab.log
``` 
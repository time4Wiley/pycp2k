#!/usr/bin/env python3
"""
Convert downloaded molecular structures to XYZ format for use with build_inputs.py
"""

from ase.io import read, write
import numpy as np

def convert_boric_acid():
    """Convert boric acid CIF to XYZ"""
    atoms = read('boric_acid.cif')
    # Extract a single molecule from the crystal
    # Boric acid is B(OH)3, so we need 1 B and 3 O atoms + 3 H atoms
    write('boric_acid.xyz', atoms)
    print(f"Converted boric acid: {len(atoms)} atoms")

def convert_ethylene_glycol():
    """Convert ethylene glycol SDF to XYZ"""
    atoms = read('ethylene_glycol.sdf')
    write('ethylene_glycol.xyz', atoms)
    print(f"Converted ethylene glycol: {len(atoms)} atoms")

def convert_formylbenzoate():
    """Convert 4-formylbenzoate SDF to XYZ"""
    atoms = read('formylbenzoate.sdf')
    write('formylbenzoate.xyz', atoms)
    print(f"Converted 4-formylbenzoate: {len(atoms)} atoms")

def create_boc_complex():
    """Create a simple boronate-diol complex"""
    # Read boric acid and ethylene glycol
    boric = read('boric_acid.xyz')
    ethylene = read('ethylene_glycol.xyz')
    
    # Simple approach: place them near each other
    # Move ethylene glycol to be close to boric acid
    ethylene.translate([5.0, 0.0, 0.0])
    
    # Combine structures
    combined = boric + ethylene
    write('boc_complex.xyz', combined)
    print(f"Created boc_complex.xyz: {len(combined)} atoms")

def create_placeholder_slab():
    """Create a placeholder slab structure"""
    # For now, create a simple placeholder since Materials Project access requires API key
    from ase.build import fcc111
    from ase import Atoms
    
    # Create a simple Ti slab as placeholder
    slab = fcc111('Ti', size=(3, 3, 4), a=4.0, vacuum=10.0)
    
    # Add some surface OH groups to mimic Ti3C2(OH)2
    positions = slab.positions
    # Add OH groups on top surface
    for i in range(3):
        for j in range(3):
            x = i * 4.0 / 3.0
            y = j * 4.0 / 3.0
            z = positions[:, 2].max() + 2.0
            
            # Add O
            slab.append('O')
            slab.positions[-1] = [x, y, z]
            
            # Add H
            slab.append('H')
            slab.positions[-1] = [x, y, z + 1.0]
    
    # Add formylbenzoate above the slab
    formyl = read('formylbenzoate.xyz')
    formyl.translate([7.5, 7.5, positions[:, 2].max() + 5.0])
    
    combined_slab = slab + formyl
    write('slab_pentamer.xyz', combined_slab)
    print(f"Created slab_pentamer.xyz: {len(combined_slab)} atoms")

if __name__ == "__main__":
    print("Converting structures to XYZ format...")
    
    convert_boric_acid()
    convert_ethylene_glycol()
    convert_formylbenzoate()
    
    print("\nCreating combined structures...")
    create_boc_complex()
    create_placeholder_slab()
    
    print("\nConversion complete! You can now run:")
    print("python build_inputs.py") 
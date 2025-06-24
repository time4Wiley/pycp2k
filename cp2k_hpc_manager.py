#!/usr/bin/env python3
"""
CP2K HPC Job Manager - Hardened Configuration for Production Use

Based on experience from PyCP2K + CP2K 2023.1 integration on HPC cluster.
Automatically generates working SLURM scripts and CP2K input files.

Author: Developed through trial-and-error on xhacnormalc partition
Date: 2025-06-25
"""

import os
import sys
import argparse
from pathlib import Path
from dataclasses import dataclass
from typing import List, Dict, Optional


@dataclass
class ClusterConfig:
    """Hardened cluster configuration based on working setup"""
    # Module configuration that works
    cp2k_module = "cp2k-2023.1-intelmpi_2021"
    pmi_library = "/opt/gridview/slurm/lib/libpmi.so"
    mpi_type = "pmi2"
    executable = "cp2k.popt"
    
    # Partition and resource defaults
    partition = "xhacnormalc"
    default_nodes = 1
    default_ntasks_per_node = 8
    default_time = "02:00:00"
    
    # Basis set files (use CP2K defaults)
    basis_set_file = "BASIS_MOLOPT"
    potential_file = "GTH_POTENTIALS"


class CP2KJobManager:
    """Manages CP2K job creation with proven HPC configuration"""
    
    def __init__(self, config: ClusterConfig = None):
        self.config = config or ClusterConfig()
        
    def create_slurm_script(self, 
                           job_name: str,
                           input_file: str,
                           output_file: str,
                           nodes: int = None,
                           ntasks_per_node: int = None,
                           time: str = None,
                           working_dir: str = ".") -> str:
        """Generate SLURM script with hardened configuration"""
        
        nodes = nodes or self.config.default_nodes
        ntasks_per_node = ntasks_per_node or self.config.default_ntasks_per_node
        time = time or self.config.default_time
        
        script = f"""#!/bin/bash
#SBATCH -J {job_name}
#SBATCH -p {self.config.partition}
#SBATCH -N {nodes}
#SBATCH --ntasks-per-node={ntasks_per_node}
#SBATCH -t {time}
#SBATCH -o %x-%j.out
#SBATCH -e %x-%j.err

# Hardened module configuration - TESTED WORKING
module purge
module load {self.config.cp2k_module}

# Critical environment variable for Intel MPI + Slurm PMI
export I_MPI_PMI_LIBRARY={self.config.pmi_library}

echo "=== {job_name} ==="
echo "Job started: $(date)"
echo "Working directory: $(pwd)"
echo "CP2K module: {self.config.cp2k_module}"

# Use proven MPI configuration: srun --mpi=pmi2 cp2k.popt
srun --mpi={self.config.mpi_type} {self.config.executable} -i {input_file} -o {output_file}

echo "Job completed: $(date)"
"""
        return script
    
    def create_cp2k_input(self,
                         project_name: str,
                         run_type: str = "GEO_OPT",
                         cutoff: int = 400,
                         cell_size: float = 15.0,
                         coordinates: List[tuple] = None,
                         include_dispersion: bool = False) -> str:
        """Generate CP2K input with version-compatible syntax"""
        
        # Default single oxygen if no coordinates provided
        if coordinates is None:
            coordinates = [("O", 0.0, 0.0, 0.0)]
            
        coord_section = "\n".join([
            f"      {atom} {x:.6f} {y:.6f} {z:.6f}" 
            for atom, x, y, z in coordinates
        ])
        
        # Determine unique atom types for KIND sections
        atom_types = list(set([coord[0] for coord in coordinates]))
        kind_sections = self._generate_kind_sections(atom_types)
        
        # XC section - dispersion optional due to CP2K 2023.1 compatibility issues
        xc_section = """    &XC
      &XC_FUNCTIONAL PBE
      &END XC_FUNCTIONAL"""
        
        if include_dispersion:
            xc_section += """
      &VDW_POTENTIAL
        POTENTIAL_TYPE PAIR_POTENTIAL
        &PAIR_POTENTIAL
          TYPE DFTD3
          PARAMETER_FILE_NAME dftd3.dat
        &END PAIR_POTENTIAL
      &END VDW_POTENTIAL"""
        
        xc_section += "\n    &END XC"
        
        # Motion section for geometry optimization (CP2K 2023.1 compatible)
        motion_section = ""
        if run_type == "GEO_OPT":
            motion_section = """
&MOTION
  &GEO_OPT
    TYPE MINIMIZATION
    MAX_FORCE 0.0005
    RMS_FORCE 0.0003
  &END GEO_OPT
&END MOTION"""
        
        input_content = f"""&GLOBAL
  PROJECT {project_name}
  RUN_TYPE {run_type}
  PRINT_LEVEL LOW
&END GLOBAL

&FORCE_EVAL
  METHOD Quickstep
  &DFT
    BASIS_SET_FILE_NAME {self.config.basis_set_file}
    POTENTIAL_FILE_NAME {self.config.potential_file}
    &MGRID
      CUTOFF {cutoff}
    &END MGRID
{xc_section}
  &END DFT

  &SUBSYS
    &CELL
      ABC {cell_size} {cell_size} {cell_size}
      PERIODIC NONE
    &END CELL

    &COORD
{coord_section}
    &END COORD

{kind_sections}
  &END SUBSYS
&END FORCE_EVAL{motion_section}"""
        
        return input_content
    
    def _generate_kind_sections(self, atom_types: List[str]) -> str:
        """Generate KIND sections for different atom types"""
        
        # Standard GTH pseudopotentials and basis sets
        standard_kinds = {
            "H": ("GTH-PBE-q1", "DZVP-MOLOPT-SR-GTH"),
            "C": ("GTH-PBE-q4", "DZVP-MOLOPT-SR-GTH"),
            "N": ("GTH-PBE-q5", "DZVP-MOLOPT-SR-GTH"),
            "O": ("GTH-PBE-q6", "DZVP-MOLOPT-SR-GTH"),
            "B": ("GTH-PBE-q3", "DZVP-MOLOPT-SR-GTH"),
        }
        
        kind_sections = []
        for atom in sorted(atom_types):
            if atom in standard_kinds:
                potential, basis = standard_kinds[atom]
                kind_sections.append(f"""    &KIND {atom}
      BASIS_SET {basis}
      POTENTIAL {potential}
    &END KIND""")
            else:
                print(f"Warning: No standard parameters for atom type {atom}")
                
        return "\n".join(kind_sections)
    
    def setup_job(self,
                 job_name: str,
                 coordinates: List[tuple],
                 output_dir: str = ".",
                 **kwargs) -> Dict[str, str]:
        """Complete job setup with SLURM script and CP2K input"""
        
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        # File names
        input_file = f"{job_name}.inp"
        output_file = f"{job_name}.out"
        slurm_file = "job.slurm"
        
        # Separate kwargs for CP2K input and SLURM script
        cp2k_kwargs = {k: v for k, v in kwargs.items() 
                       if k in ['run_type', 'cutoff', 'cell_size', 'include_dispersion']}
        slurm_kwargs = {k: v for k, v in kwargs.items() 
                        if k in ['nodes', 'ntasks_per_node', 'time']}
        
        # Generate content
        cp2k_input = self.create_cp2k_input(
            project_name=job_name,
            coordinates=coordinates,
            **cp2k_kwargs
        )
        
        slurm_script = self.create_slurm_script(
            job_name=job_name,
            input_file=input_file,
            output_file=output_file,
            **slurm_kwargs
        )
        
        # Write files
        with open(output_path / input_file, 'w') as f:
            f.write(cp2k_input)
            
        with open(output_path / slurm_file, 'w') as f:
            f.write(slurm_script)
            
        return {
            "input_file": str(output_path / input_file),
            "slurm_file": str(output_path / slurm_file),
            "output_dir": str(output_path)
        }


def main():
    """Command line interface"""
    parser = argparse.ArgumentParser(description="CP2K HPC Job Manager")
    parser.add_argument("job_name", help="Job name")
    parser.add_argument("--coords", help="Coordinate file (XYZ format)")
    parser.add_argument("--output-dir", "-o", default=".", help="Output directory")
    parser.add_argument("--cutoff", type=int, default=400, help="Plane wave cutoff (eV)")
    parser.add_argument("--cell-size", type=float, default=15.0, help="Cell size (Å)")
    parser.add_argument("--dispersion", action="store_true", help="Include D3 dispersion")
    parser.add_argument("--run-type", default="GEO_OPT", choices=["ENERGY", "GEO_OPT", "MD"])
    parser.add_argument("--nodes", type=int, default=1, help="Number of nodes")
    parser.add_argument("--ntasks", type=int, default=8, help="Tasks per node")
    parser.add_argument("--time", default="02:00:00", help="Wall time")
    
    args = parser.parse_args()
    
    # Parse coordinates
    coordinates = [("O", 0.0, 0.0, 0.0)]  # Default
    if args.coords:
        coordinates = parse_xyz_file(args.coords)
    
    # Setup job
    manager = CP2KJobManager()
    files = manager.setup_job(
        job_name=args.job_name,
        coordinates=coordinates,
        output_dir=args.output_dir,
        run_type=args.run_type,
        cutoff=args.cutoff,
        cell_size=args.cell_size,
        include_dispersion=args.dispersion,
        nodes=args.nodes,
        ntasks_per_node=args.ntasks,
        time=args.time
    )
    
    print("✅ CP2K HPC job setup complete:")
    print(f"   Input: {files['input_file']}")
    print(f"   SLURM: {files['slurm_file']}")
    print(f"   Submit: cd {files['output_dir']} && sbatch job.slurm")


def parse_xyz_file(filename: str) -> List[tuple]:
    """Parse XYZ coordinate file"""
    coordinates = []
    with open(filename, 'r') as f:
        lines = f.readlines()
        n_atoms = int(lines[0].strip())
        for i in range(2, 2 + n_atoms):
            parts = lines[i].strip().split()
            atom = parts[0]
            x, y, z = map(float, parts[1:4])
            coordinates.append((atom, x, y, z))
    return coordinates


if __name__ == "__main__":
    main() 
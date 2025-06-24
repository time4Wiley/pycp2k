#!/usr/bin/env python3
"""
create_md_test.py
Create molecular dynamics inputs for minimal test systems to verify the same
interaction physics as the full research system but with much lower cost.

Based on CP2K MD best practices from: https://manual.cp2k.org/trunk/methods/sampling/molecular_dynamics.html
"""

import sys
sys.path.insert(0, '..')
from pycp2k import CP2K
from ase.io import read

def create_md_input(atoms, project_name, temperature=300, timestep=1.0, total_steps=1000):
    """
    Create CP2K molecular dynamics input with optimized settings for fast local testing.
    
    Following CP2K manual recommendations:
    - Use PS extrapolation with order 3 for continuous density changes
    - NVE ensemble for energy conservation testing  
    - 1 fs timestep for good energy conservation
    - TEMP_TOL for equilibration
    """
    
    inp = CP2K()
    
    # Global settings
    inp.CP2K_INPUT.GLOBAL.Project_name = project_name
    inp.CP2K_INPUT.GLOBAL.Run_type = "MD"
    inp.CP2K_INPUT.GLOBAL.Print_level = "MEDIUM"
    
    # Force evaluation (same as geometry optimization)
    force_eval = inp.CP2K_INPUT.FORCE_EVAL_add()
    force_eval.Method = "Quickstep"
    
    # DFT settings - optimized for MD
    dft = force_eval.DFT
    dft.Basis_set_file_name = "BASIS_MOLOPT"
    dft.Potential_file_name = "GTH_POTENTIALS"
    
    # Grid settings (slightly reduced for speed)
    dft.MGRID.Cutoff = 280  # Lower cutoff for MD testing
    dft.MGRID.Rel_cutoff = 40  # Lower rel_cutoff for MD
    
    # SCF settings optimized for MD
    dft.SCF.Eps_scf = 5.0e-6  # Slightly relaxed for MD
    dft.SCF.Max_scf = 30
    dft.SCF.OT.Preconditioner = "FULL_SINGLE_INVERSE"
    dft.SCF.OT.Minimizer = "DIIS"
    
    # PS extrapolation for MD (CP2K manual recommendation)
    dft.SCF.Scf_guess = "PS"  
    dft.QS.Extrapolation = "PS"
    dft.QS.Extrapolation_order = 3
    
    # XC functional: PBE + D3 (same as research system)
    dft.XC.XC_FUNCTIONAL.Section_parameters = "PBE"
    dft.XC.VDW_POTENTIAL.Potential_type = "PAIR_POTENTIAL"
    pair_pot = dft.XC.VDW_POTENTIAL.PAIR_POTENTIAL_add()
    pair_pot.Type = "DFTD3"
    pair_pot.Reference_functional = "PBE"
    
    # Cell settings
    cell = force_eval.SUBSYS.CELL
    cell_size = 12.0
    cell.A = [cell_size, 0, 0]
    cell.B = [0, cell_size, 0]
    cell.C = [0, 0, cell_size]
    cell.Periodic = "XYZ"
    
    # Add coordinates
    for symbol, pos in zip(atoms.get_chemical_symbols(), atoms.get_positions()):
        force_eval.SUBSYS.COORD.Default_keyword.append([symbol, pos[0], pos[1], pos[2]])
    
    # Basis sets and potentials
    elements = set(atoms.get_chemical_symbols())
    for element in elements:
        kind = force_eval.SUBSYS.KIND_add()
        kind.Section_parameters = element
        if element == 'Ti':
            kind.Basis_set = "DZVP-MOLOPT-SR-GTH"
            kind.Potential = "GTH-PBE-q12"
        elif element == 'C':
            kind.Basis_set = "DZVP-MOLOPT-GTH"
            kind.Potential = "GTH-PBE-q4"
        elif element == 'B':
            kind.Basis_set = "DZVP-MOLOPT-GTH"
            kind.Potential = "GTH-PBE-q3"
        elif element == 'O':
            kind.Basis_set = "DZVP-MOLOPT-GTH"
            kind.Potential = "GTH-PBE-q6"
        elif element == 'H':
            kind.Basis_set = "DZVP-MOLOPT-GTH"
            kind.Potential = "GTH-PBE-q1"
    
    # MD settings
    motion = inp.CP2K_INPUT.MOTION
    md = motion.MD
    
    # Basic MD parameters
    md.Ensemble = "NVE"  # For energy conservation testing
    md.Steps = total_steps
    md.Timestep = timestep  # 1 fs recommended
    md.Temperature = temperature
    
    # Temperature tolerance for equilibration (CP2K manual recommendation)
    md.Temp_tol = 50  # K - allows crude velocity rescaling when far from target
    
    # Thermostat settings (for initial equilibration)
    md.THERMOSTAT.Type = "CSVR"  # Canonical sampling through velocity rescaling
    md.THERMOSTAT.CSVR.Timecon = 100.0  # fs
    
    # Print settings for analysis (use PRINT_add for MOTION)
    print_section = motion.PRINT_add()
    print_section.TRAJECTORY.EACH.Md = 10  # Save every 10 steps
    print_section.VELOCITIES.EACH.Md = 10
    print_section.FORCES.EACH.Md = 10
    print_section.RESTART.EACH.Md = 100
    
    return inp

def create_equilibration_input(atoms, project_name):
    """
    Create equilibration run using Langevin dynamics for faster equilibration.
    Following CP2K manual: Use LANGEVIN with small gamma for equilibration.
    """
    
    inp = create_md_input(atoms, f"{project_name}_equilib", temperature=300, timestep=1.0, total_steps=500)
    
    # Change to Langevin for faster equilibration
    md = inp.CP2K_INPUT.MOTION.MD
    md.Ensemble = "LANGEVIN"
    md.LANGEVIN.Gamma = 0.001  # 1/fs - small gamma for gentle equilibration
    md.LANGEVIN.Noisy_gamma = 0.001
    
    # Higher temperature tolerance for equilibration
    md.Temp_tol = 100  # K
    
    return inp

def generate_md_test_suite():
    """Generate complete MD test suite for all minimal systems"""
    
    print("🚀 Generating MD test suite for minimal systems...")
    print("=" * 60)
    
    systems = [
        ('minimal_boronate_diol.xyz', 'Tests B-O bond dynamics'),
        ('minimal_ti3c2_surface.xyz', 'Tests MXene surface dynamics'),
        ('minimal_combined.xyz', 'Tests surface-molecule interactions')
    ]
    
    for xyz_file, description in systems:
        try:
            atoms = read(xyz_file)
            base_name = xyz_file.replace('.xyz', '')
            
            print(f"🧬 {base_name} ({len(atoms)} atoms)")
            print(f"   🎯 {description}")
            
            # Create equilibration input
            equil_inp = create_equilibration_input(atoms, base_name)
            equil_file = f"{base_name}_equilib.inp"
            equil_inp.write_input_file(equil_file)
            print(f"   📄 Equilibration: {equil_file}")
            
            # Create production MD input
            md_inp = create_md_input(atoms, f"{base_name}_md", temperature=300, timestep=1.0, total_steps=1000)
            md_file = f"{base_name}_md.inp"
            md_inp.write_input_file(md_file)
            print(f"   📄 Production MD: {md_file}")
            
            # Estimate computational time
            # Rough estimate: ~15 atoms = 1-2 min/step for local CPU
            time_per_step = max(1, len(atoms) / 10)  # seconds
            total_time = (500 + 1000) * time_per_step / 60  # minutes
            print(f"   ⏱️  Estimated time: {total_time:.1f} minutes on local CPU")
            print()
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
            print()
    
    # Create analysis script
    create_md_analysis_script()
    
    print("🎉 MD test suite generated!")
    print("\\n📋 Usage:")
    print("   1. Run equilibration: cp2k.sopt -in minimal_combined_equilib.inp")
    print("   2. Run production MD: cp2k.sopt -in minimal_combined_md.inp") 
    print("   3. Analyze results: python analyze_md_results.py")
    print("\\n🎯 What to check:")
    print("   - Energy conservation in .ener files")
    print("   - Temperature stability")
    print("   - Bond formation/breaking events")
    print("   - System equilibration")

def create_md_analysis_script():
    """Create script for analyzing MD results"""
    
    analysis_script = '''#!/usr/bin/env python3
"""
analyze_md_results.py
Analyze MD results for energy conservation and system behavior.
"""

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

def parse_ener_file(ener_file):
    """Parse CP2K .ener file"""
    try:
        data = np.loadtxt(ener_file, skiprows=1)
        # Columns: step, time[fs], kinetic[hartree], temp[K], potential[hartree], total[hartree], cpu_time[s]
        return {
            'step': data[:, 0],
            'time': data[:, 1],
            'kinetic': data[:, 2],
            'temperature': data[:, 3], 
            'potential': data[:, 4],
            'total': data[:, 5],
            'cpu_time': data[:, 6]
        }
    except:
        return None

def analyze_energy_conservation(data, system_name):
    """Analyze energy conservation quality"""
    
    total_energy = data['total']
    temperature = data['temperature']
    time = data['time']
    
    # Energy drift analysis
    energy_drift = (total_energy[-1] - total_energy[0]) / len(total_energy) * 1000  # per ps
    energy_fluctuation = np.std(total_energy)
    
    # Convert to temperature units (1 hartree ≈ 315775 K)
    drift_temp = energy_drift * 315775
    fluct_temp = energy_fluctuation * 315775
    
    # Temperature statistics
    avg_temp = np.mean(temperature)
    temp_std = np.std(temperature)
    
    print(f"🔬 {system_name} Analysis:")
    print(f"   📊 Energy Conservation:")
    print(f"      Drift: {drift_temp:.2f} K/ps ({energy_drift:.2e} hartree/ps)")
    print(f"      Fluctuation: {fluct_temp:.2f} K ({energy_fluctuation:.2e} hartree)")
    print(f"   🌡️  Temperature:")
    print(f"      Average: {avg_temp:.1f} K")
    print(f"      Std Dev: {temp_std:.1f} K")
    
    # Quality assessment
    if abs(drift_temp) < 1.0 and fluct_temp < 10.0:
        print(f"   ✅ Excellent energy conservation")
    elif abs(drift_temp) < 5.0 and fluct_temp < 50.0:
        print(f"   ✅ Good energy conservation") 
    else:
        print(f"   ⚠️  Poor energy conservation - check timestep/convergence")
    
    return drift_temp, fluct_temp, avg_temp, temp_std

def plot_md_results(data, system_name):
    """Create plots for MD analysis"""
    
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    fig.suptitle(f'MD Analysis: {system_name}', fontsize=14)
    
    time_ps = data['time'] / 1000  # Convert fs to ps
    
    # Energy vs time
    axes[0,0].plot(time_ps, data['total'], 'b-', linewidth=1)
    axes[0,0].set_xlabel('Time (ps)')
    axes[0,0].set_ylabel('Total Energy (hartree)')
    axes[0,0].set_title('Energy Conservation')
    axes[0,0].grid(True, alpha=0.3)
    
    # Temperature vs time
    axes[0,1].plot(time_ps, data['temperature'], 'r-', linewidth=1)
    axes[0,1].set_xlabel('Time (ps)')
    axes[0,1].set_ylabel('Temperature (K)')
    axes[0,1].set_title('Temperature Fluctuations')
    axes[0,1].grid(True, alpha=0.3)
    
    # Energy components
    axes[1,0].plot(time_ps, data['kinetic'], 'g-', label='Kinetic', linewidth=1)
    axes[1,0].plot(time_ps, data['potential'], 'm-', label='Potential', linewidth=1)
    axes[1,0].set_xlabel('Time (ps)')
    axes[1,0].set_ylabel('Energy (hartree)')
    axes[1,0].set_title('Energy Components')
    axes[1,0].legend()
    axes[1,0].grid(True, alpha=0.3)
    
    # Energy drift
    energy_relative = (data['total'] - data['total'][0]) / abs(data['total'][0]) * 100
    axes[1,1].plot(time_ps, energy_relative, 'k-', linewidth=1)
    axes[1,1].set_xlabel('Time (ps)')
    axes[1,1].set_ylabel('Energy Drift (%)')
    axes[1,1].set_title('Relative Energy Drift')
    axes[1,1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plot_file = f'{system_name}_md_analysis.png'
    plt.savefig(plot_file, dpi=300, bbox_inches='tight')
    plt.close()
    
    return plot_file

def main():
    """Analyze all MD results"""
    
    print("📊 Analyzing MD Results...")
    print("=" * 40)
    
    systems = [
        'minimal_boronate_diol',
        'minimal_ti3c2_surface', 
        'minimal_combined'
    ]
    
    for system in systems:
        # Check for .ener files
        ener_files = list(Path('.').glob(f'{system}*-1.ener'))
        
        if ener_files:
            for ener_file in ener_files:
                data = parse_ener_file(ener_file)
                if data is not None:
                    # Analyze
                    analyze_energy_conservation(data, system)
                    
                    # Plot
                    plot_file = plot_md_results(data, system)
                    print(f"   📈 Plot saved: {plot_file}")
                    print()
                else:
                    print(f"   ❌ Could not parse {ener_file}")
        else:
            print(f"   ⚠️  No .ener files found for {system}")
            print("      Run MD simulation first!")
    
    print("🎉 Analysis complete!")

if __name__ == "__main__":
    main()
'''
    
    with open('analyze_md_results.py', 'w') as f:
        f.write(analysis_script)
    
    print("📊 Created analyze_md_results.py for result analysis")

if __name__ == "__main__":
    generate_md_test_suite() 
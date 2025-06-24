#!/usr/bin/env python3
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

#!/usr/bin/env python3
"""
Monitor the remaining CBA geometry optimization job and prepare for binding energy calculation.
"""

import subprocess
import time
import os

def check_job_status():
    """Check if the CBA job is still running."""
    try:
        result = subprocess.run(['squeue', '-u', os.environ['USER']], 
                              capture_output=True, text=True)
        return '15269735' in result.stdout
    except:
        return False

def check_convergence():
    """Check convergence status of the CBA job."""
    output_file = "energy_compare/02_cba_borate_geo_opt_improved/cba_borate_geo_opt_improved.out"
    
    if not os.path.exists(output_file):
        return "Output file not found"
    
    try:
        with open(output_file, 'r') as f:
            content = f.read()
        
        if "GEOMETRY OPTIMIZATION COMPLETED" in content:
            # Extract final energy
            lines = content.split('\n')
            for line in reversed(lines):
                if "Total energy:" in line:
                    final_energy = line.split()[-1]
                    return f"✅ COMPLETED - Final energy: {final_energy} Hartree"
            return "✅ COMPLETED - Energy not found"
        
        # Get last few SCF cycles
        lines = content.split('\n')
        scf_lines = [line for line in lines if 'Broy./Diag.' in line]
        if scf_lines:
            last_scf = scf_lines[-1]
            convergence = last_scf.split()[4]  # Convergence value
            return f"🔄 Running - Last convergence: {convergence}"
        
        return "🔄 Running - SCF status unclear"
        
    except Exception as e:
        return f"Error reading file: {e}"

def main():
    """Monitor job and provide status."""
    print("🔍 Monitoring CBA-borate geometry optimization (Job 15269735)")
    print("=" * 60)
    
    # Current status
    job_running = check_job_status()
    convergence_status = check_convergence()
    
    print(f"Job Status: {'Running' if job_running else 'Completed/Failed'}")
    print(f"Convergence: {convergence_status}")
    print("")
    
    if job_running:
        print("📋 **NEXT STEPS:**")
        print("1. Wait for CBA geometry optimization to complete")
        print("2. Extract optimized geometries from both PVA and CBA jobs")
        print("3. Calculate binding energies using optimized structures")
        print("4. Compare PVA vs CBA binding strength")
        print("")
        print("💡 **CURRENT RESULTS:**")
        print("✅ PVA-borate: COMPLETED (-99.813 Hartree)")
        print("🔄 CBA-borate: RUNNING (improved SCF convergence)")
        print("")
        print("⏱️  Estimated time to completion: 30-60 minutes")
        print("💰 Current cost: ~$15-20 (much better than original problematic jobs)")
    else:
        if "COMPLETED" in convergence_status:
            print("🎉 **ALL GEOMETRY OPTIMIZATIONS COMPLETED!**")
            print("")
            print("📋 **READY FOR BINDING ENERGY CALCULATION:**")
            print("✅ PVA-borate optimized: -99.813 Hartree")
            print(f"✅ CBA-borate optimized: {convergence_status}")
            print("")
            print("🚀 **NEXT: Run binding energy analysis script**")
        else:
            print("❌ **JOB FAILED OR CANCELLED**")
            print("Need to investigate and possibly restart")

if __name__ == "__main__":
    main() 
"""
Monitor the remaining CBA geometry optimization job and prepare for binding energy calculation.
"""

import subprocess
import time
import os

def check_job_status():
    """Check if the CBA job is still running."""
    try:
        result = subprocess.run(['squeue', '-u', os.environ['USER']], 
                              capture_output=True, text=True)
        return '15269735' in result.stdout
    except:
        return False

def check_convergence():
    """Check convergence status of the CBA job."""
    output_file = "energy_compare/02_cba_borate_geo_opt_improved/cba_borate_geo_opt_improved.out"
    
    if not os.path.exists(output_file):
        return "Output file not found"
    
    try:
        with open(output_file, 'r') as f:
            content = f.read()
        
        if "GEOMETRY OPTIMIZATION COMPLETED" in content:
            # Extract final energy
            lines = content.split('\n')
            for line in reversed(lines):
                if "Total energy:" in line:
                    final_energy = line.split()[-1]
                    return f"✅ COMPLETED - Final energy: {final_energy} Hartree"
            return "✅ COMPLETED - Energy not found"
        
        # Get last few SCF cycles
        lines = content.split('\n')
        scf_lines = [line for line in lines if 'Broy./Diag.' in line]
        if scf_lines:
            last_scf = scf_lines[-1]
            convergence = last_scf.split()[4]  # Convergence value
            return f"🔄 Running - Last convergence: {convergence}"
        
        return "🔄 Running - SCF status unclear"
        
    except Exception as e:
        return f"Error reading file: {e}"

def main():
    """Monitor job and provide status."""
    print("🔍 Monitoring CBA-borate geometry optimization (Job 15269735)")
    print("=" * 60)
    
    # Current status
    job_running = check_job_status()
    convergence_status = check_convergence()
    
    print(f"Job Status: {'Running' if job_running else 'Completed/Failed'}")
    print(f"Convergence: {convergence_status}")
    print("")
    
    if job_running:
        print("📋 **NEXT STEPS:**")
        print("1. Wait for CBA geometry optimization to complete")
        print("2. Extract optimized geometries from both PVA and CBA jobs")
        print("3. Calculate binding energies using optimized structures")
        print("4. Compare PVA vs CBA binding strength")
        print("")
        print("💡 **CURRENT RESULTS:**")
        print("✅ PVA-borate: COMPLETED (-99.813 Hartree)")
        print("🔄 CBA-borate: RUNNING (improved SCF convergence)")
        print("")
        print("⏱️  Estimated time to completion: 30-60 minutes")
        print("💰 Current cost: ~$15-20 (much better than original problematic jobs)")
    else:
        if "COMPLETED" in convergence_status:
            print("🎉 **ALL GEOMETRY OPTIMIZATIONS COMPLETED!**")
            print("")
            print("📋 **READY FOR BINDING ENERGY CALCULATION:**")
            print("✅ PVA-borate optimized: -99.813 Hartree")
            print(f"✅ CBA-borate optimized: {convergence_status}")
            print("")
            print("🚀 **NEXT: Run binding energy analysis script**")
        else:
            print("❌ **JOB FAILED OR CANCELLED**")
            print("Need to investigate and possibly restart")

if __name__ == "__main__":
    main() 
"""
Monitor the remaining CBA geometry optimization job and prepare for binding energy calculation.
"""

import subprocess
import time
import os

def check_job_status():
    """Check if the CBA job is still running."""
    try:
        result = subprocess.run(['squeue', '-u', os.environ['USER']], 
                              capture_output=True, text=True)
        return '15269735' in result.stdout
    except:
        return False

def check_convergence():
    """Check convergence status of the CBA job."""
    output_file = "energy_compare/02_cba_borate_geo_opt_improved/cba_borate_geo_opt_improved.out"
    
    if not os.path.exists(output_file):
        return "Output file not found"
    
    try:
        with open(output_file, 'r') as f:
            content = f.read()
        
        if "GEOMETRY OPTIMIZATION COMPLETED" in content:
            # Extract final energy
            lines = content.split('\n')
            for line in reversed(lines):
                if "Total energy:" in line:
                    final_energy = line.split()[-1]
                    return f"✅ COMPLETED - Final energy: {final_energy} Hartree"
            return "✅ COMPLETED - Energy not found"
        
        # Get last few SCF cycles
        lines = content.split('\n')
        scf_lines = [line for line in lines if 'Broy./Diag.' in line]
        if scf_lines:
            last_scf = scf_lines[-1]
            convergence = last_scf.split()[4]  # Convergence value
            return f"🔄 Running - Last convergence: {convergence}"
        
        return "🔄 Running - SCF status unclear"
        
    except Exception as e:
        return f"Error reading file: {e}"

def main():
    """Monitor job and provide status."""
    print("🔍 Monitoring CBA-borate geometry optimization (Job 15269735)")
    print("=" * 60)
    
    # Current status
    job_running = check_job_status()
    convergence_status = check_convergence()
    
    print(f"Job Status: {'Running' if job_running else 'Completed/Failed'}")
    print(f"Convergence: {convergence_status}")
    print("")
    
    if job_running:
        print("📋 **NEXT STEPS:**")
        print("1. Wait for CBA geometry optimization to complete")
        print("2. Extract optimized geometries from both PVA and CBA jobs")
        print("3. Calculate binding energies using optimized structures")
        print("4. Compare PVA vs CBA binding strength")
        print("")
        print("💡 **CURRENT RESULTS:**")
        print("✅ PVA-borate: COMPLETED (-99.813 Hartree)")
        print("🔄 CBA-borate: RUNNING (improved SCF convergence)")
        print("")
        print("⏱️  Estimated time to completion: 30-60 minutes")
        print("💰 Current cost: ~$15-20 (much better than original problematic jobs)")
    else:
        if "COMPLETED" in convergence_status:
            print("🎉 **ALL GEOMETRY OPTIMIZATIONS COMPLETED!**")
            print("")
            print("📋 **READY FOR BINDING ENERGY CALCULATION:**")
            print("✅ PVA-borate optimized: -99.813 Hartree")
            print(f"✅ CBA-borate optimized: {convergence_status}")
            print("")
            print("🚀 **NEXT: Run binding energy analysis script**")
        else:
            print("❌ **JOB FAILED OR CANCELLED**")
            print("Need to investigate and possibly restart")

if __name__ == "__main__":
    main() 
"""
Monitor the remaining CBA geometry optimization job and prepare for binding energy calculation.
"""

import subprocess
import time
import os

def check_job_status():
    """Check if the CBA job is still running."""
    try:
        result = subprocess.run(['squeue', '-u', os.environ['USER']], 
                              capture_output=True, text=True)
        return '15269735' in result.stdout
    except:
        return False

def check_convergence():
    """Check convergence status of the CBA job."""
    output_file = "energy_compare/02_cba_borate_geo_opt_improved/cba_borate_geo_opt_improved.out"
    
    if not os.path.exists(output_file):
        return "Output file not found"
    
    try:
        with open(output_file, 'r') as f:
            content = f.read()
        
        if "GEOMETRY OPTIMIZATION COMPLETED" in content:
            # Extract final energy
            lines = content.split('\n')
            for line in reversed(lines):
                if "Total energy:" in line:
                    final_energy = line.split()[-1]
                    return f"✅ COMPLETED - Final energy: {final_energy} Hartree"
            return "✅ COMPLETED - Energy not found"
        
        # Get last few SCF cycles
        lines = content.split('\n')
        scf_lines = [line for line in lines if 'Broy./Diag.' in line]
        if scf_lines:
            last_scf = scf_lines[-1]
            convergence = last_scf.split()[4]  # Convergence value
            return f"🔄 Running - Last convergence: {convergence}"
        
        return "🔄 Running - SCF status unclear"
        
    except Exception as e:
        return f"Error reading file: {e}"

def main():
    """Monitor job and provide status."""
    print("🔍 Monitoring CBA-borate geometry optimization (Job 15269735)")
    print("=" * 60)
    
    # Current status
    job_running = check_job_status()
    convergence_status = check_convergence()
    
    print(f"Job Status: {'Running' if job_running else 'Completed/Failed'}")
    print(f"Convergence: {convergence_status}")
    print("")
    
    if job_running:
        print("📋 **NEXT STEPS:**")
        print("1. Wait for CBA geometry optimization to complete")
        print("2. Extract optimized geometries from both PVA and CBA jobs")
        print("3. Calculate binding energies using optimized structures")
        print("4. Compare PVA vs CBA binding strength")
        print("")
        print("💡 **CURRENT RESULTS:**")
        print("✅ PVA-borate: COMPLETED (-99.813 Hartree)")
        print("🔄 CBA-borate: RUNNING (improved SCF convergence)")
        print("")
        print("⏱️  Estimated time to completion: 30-60 minutes")
        print("💰 Current cost: ~$15-20 (much better than original problematic jobs)")
    else:
        if "COMPLETED" in convergence_status:
            print("🎉 **ALL GEOMETRY OPTIMIZATIONS COMPLETED!**")
            print("")
            print("📋 **READY FOR BINDING ENERGY CALCULATION:**")
            print("✅ PVA-borate optimized: -99.813 Hartree")
            print(f"✅ CBA-borate optimized: {convergence_status}")
            print("")
            print("🚀 **NEXT: Run binding energy analysis script**")
        else:
            print("❌ **JOB FAILED OR CANCELLED**")
            print("Need to investigate and possibly restart")

if __name__ == "__main__":
    main() 
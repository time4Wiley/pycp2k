#!/usr/bin/env python3
"""
Monitor Slurm jobs for binding energy calculations
- Check job status with squeue
- Parse output files for energies
- Report progress and results
"""

import subprocess
import os
import re
import time
from datetime import datetime


def run_command(cmd):
    """Run shell command and return output"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.returncode, result.stdout.strip(), result.stderr.strip()
    except Exception as e:
        return 1, "", str(e)


def check_job_status():
    """Check status of running jobs"""
    ret, stdout, stderr = run_command("squeue -u $USER")
    if ret != 0:
        return "Error checking jobs", []
    
    lines = stdout.split('\n')
    if len(lines) <= 1:
        return "No jobs running", []
    
    jobs = []
    for line in lines[1:]:  # Skip header
        parts = line.split()
        if len(parts) >= 8:
            job_id = parts[0]
            name = parts[2]
            status = parts[4] 
            time_used = parts[5]
            jobs.append({
                'id': job_id,
                'name': name, 
                'status': status,
                'time': time_used
            })
    
    return "Jobs found", jobs


def parse_cp2k_energy(output_file):
    """Extract final energy from CP2K output"""
    if not os.path.exists(output_file):
        return None, "Output file not found"
    
    try:
        with open(output_file, 'r') as f:
            content = f.read()
        
        # Look for final SCF energy
        energy_pattern = r"Total FORCE_EVAL \( QS \) energy.*?:\s*([-\d\.E\+\-]+)"
        matches = re.findall(energy_pattern, content)
        
        if matches:
            return float(matches[-1]), "Converged"
        
        # Check if still running
        if "SCF run converged" in content:
            return None, "Converged but energy not parsed"
        elif "SCF" in content:
            return None, "SCF running"
        else:
            return None, "Not started"
            
    except Exception as e:
        return None, f"Parse error: {e}"


def monitor_calculations():
    """Monitor both PVA and CBA calculations"""
    
    calculations = [
        {
            'name': 'PVA-borate',
            'dir': 'energy_compare/01_pva_borate',
            'output': 'pva_borate.out'
        },
        {
            'name': 'CBA-borate', 
            'dir': 'energy_compare/02_cba_borate',
            'output': 'cba_borate.out'
        }
    ]
    
    print(f"🔍 Monitoring binding energy calculations - {datetime.now().strftime('%H:%M:%S')}")
    print("=" * 70)
    
    # Check job queue
    status, jobs = check_job_status()
    print(f"📋 Job Queue Status: {status}")
    
    if jobs:
        print("Running jobs:")
        for job in jobs:
            if any(calc['name'].lower().replace('-', '_') in job['name'].lower() for calc in calculations):
                print(f"  🔶 {job['name']} (ID: {job['id']}) - {job['status']} - {job['time']}")
    else:
        print("  No relevant jobs in queue")
    
    print("\n📊 Calculation Progress:")
    
    for calc in calculations:
        output_path = os.path.join(calc['dir'], calc['output'])
        energy, status = parse_cp2k_energy(output_path)
        
        if energy is not None:
            print(f"  ✅ {calc['name']}: {energy:.6f} au ({status})")
        else:
            print(f"  ⏳ {calc['name']}: {status}")
    
    # Check for completion
    completed = []
    for calc in calculations:
        output_path = os.path.join(calc['dir'], calc['output'])
        energy, status = parse_cp2k_energy(output_path)
        if energy is not None:
            completed.append({'name': calc['name'], 'energy': energy})
    
    if len(completed) == 2:
        print("\n🎉 Both calculations completed!")
        pva_energy = next(c['energy'] for c in completed if 'PVA' in c['name'])
        cba_energy = next(c['energy'] for c in completed if 'CBA' in c['name'])
        
        print(f"\n📈 Binding Energy Comparison:")
        print(f"  PVA-borate:  {pva_energy:.6f} au")
        print(f"  CBA-borate:  {cba_energy:.6f} au")
        print(f"  Difference:  {abs(pva_energy - cba_energy):.6f} au")
        print(f"               {abs(pva_energy - cba_energy) * 627.5:.2f} kcal/mol")
        
        if cba_energy < pva_energy:
            print("  → CBA-borate is more stable!")
        else:
            print("  → PVA-borate is more stable!")
    
    print("=" * 70)


def continuous_monitor(interval=30):
    """Monitor continuously until both jobs complete"""
    try:
        while True:
            monitor_calculations()
            
            # Check if both completed
            pva_energy, _ = parse_cp2k_energy('energy_compare/01_pva_borate/pva_borate.out')
            cba_energy, _ = parse_cp2k_energy('energy_compare/02_cba_borate/cba_borate.out')
            
            if pva_energy is not None and cba_energy is not None:
                print("\n✅ All calculations complete! Monitoring finished.")
                break
            
            print(f"\n⏱️  Next check in {interval} seconds... (Ctrl+C to stop)")
            time.sleep(interval)
            
    except KeyboardInterrupt:
        print("\n\n⏹️  Monitoring stopped by user")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--continuous":
        continuous_monitor()
    else:
        monitor_calculations() 
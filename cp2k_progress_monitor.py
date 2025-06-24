#!/usr/bin/env python3
"""
CP2K Progress Monitor and CPU Hours Calculator

This script monitors CP2K geometry optimization jobs, extracts progress information,
and calculates CPU hours consumed. Works with both running and completed jobs.

Usage:
    python3 cp2k_progress_monitor.py [job_directory]
    python3 cp2k_progress_monitor.py --all-jobs  # Monitor all jobs in energy_compare/
"""

import os
import sys
import re
import subprocess
import time
from datetime import datetime, timedelta
from pathlib import Path
import argparse

class CP2KProgressMonitor:
    def __init__(self):
        self.job_patterns = {
            'slurm_output': r'.*_(\d+)\.out$',
            'cp2k_output': r'.*\.out$',
            'slurm_error': r'.*_(\d+)\.err$'
        }
        
    def get_job_info_from_squeue(self, job_id=None):
        """Get job information from SLURM queue"""
        try:
            if job_id:
                cmd = ['squeue', '-j', str(job_id), '-o', '%.10i %.15j %.8u %.2t %.10M %.6D %R %.15S']
            else:
                cmd = ['squeue', '-u', os.getenv('USER', 'acdad3pzwp'), '-o', '%.10i %.15j %.8u %.2t %.10M %.6D %R %.15S']
            
            result = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = result.communicate()
            
            if result.returncode == 0:
                lines = stdout.decode().strip().split('\n')
                if len(lines) > 1:  # Skip header
                    jobs = []
                    for line in lines[1:]:
                        parts = line.split()
                        if len(parts) >= 7:
                            job_info = {
                                'job_id': parts[0],
                                'job_name': parts[1],
                                'user': parts[2],
                                'status': parts[3],
                                'time_elapsed': parts[4],
                                'nodes': parts[5],
                                'node_list': parts[6],
                                'start_time': parts[7] if len(parts) > 7 else 'N/A'
                            }
                            jobs.append(job_info)
                    return jobs
            return []
        except Exception as e:
            print(f"Error getting job info: {e}")
            return []

    def parse_slurm_time(self, time_str):
        """Parse SLURM time format (e.g., '43:34', '1-02:30:45') to total minutes"""
        if not time_str or time_str == 'N/A':
            return 0
        
        try:
            # Handle day-hour:minute:second format
            if '-' in time_str:
                days, hms = time_str.split('-')
                days = int(days)
                if ':' in hms:
                    time_parts = hms.split(':')
                    if len(time_parts) == 3:
                        hours, minutes, seconds = map(int, time_parts)
                    elif len(time_parts) == 2:
                        hours, minutes = map(int, time_parts)
                        seconds = 0
                    else:
                        hours = int(time_parts[0])
                        minutes = seconds = 0
                else:
                    hours = int(hms)
                    minutes = seconds = 0
                total_minutes = days * 24 * 60 + hours * 60 + minutes + seconds / 60
            else:
                # Handle hour:minute or hour:minute:second format
                time_parts = time_str.split(':')
                if len(time_parts) == 3:
                    hours, minutes, seconds = map(int, time_parts)
                    total_minutes = hours * 60 + minutes + seconds / 60
                elif len(time_parts) == 2:
                    hours, minutes = map(int, time_parts)
                    total_minutes = hours * 60 + minutes
                else:
                    total_minutes = int(time_parts[0]) * 60  # Assume hours
            
            return total_minutes
        except Exception as e:
            print(f"Error parsing time '{time_str}': {e}")
            return 0

    def get_slurm_job_details(self, job_id):
        """Get detailed job information from sacct"""
        try:
            cmd = ['sacct', '-j', str(job_id), '--format=JobID,JobName,State,Start,End,Elapsed,NCPUS,NNodes', '--parsable2']
            result = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = result.communicate()
            
            if result.returncode == 0:
                lines = stdout.decode().strip().split('\n')
                if len(lines) > 1:
                    # Parse the main job (not job steps)
                    for line in lines[1:]:
                        parts = line.split('|')
                        if len(parts) >= 8 and not '.' in parts[0]:  # Main job, not job step
                            return {
                                'job_id': parts[0],
                                'job_name': parts[1],
                                'state': parts[2],
                                'start_time': parts[3],
                                'end_time': parts[4],
                                'elapsed': parts[5],
                                'ncpus': parts[6],
                                'nnodes': parts[7]
                            }
            return None
        except Exception as e:
            print(f"Error getting detailed job info: {e}")
            return None

    def analyze_cp2k_output(self, output_file):
        """Analyze CP2K output file for progress information"""
        if not os.path.exists(output_file):
            return {
                'exists': False,
                'size_mb': 0,
                'scf_steps': 0,
                'geo_steps': 0,
                'current_energy': None,
                'converged': False,
                'last_update': None
            }
        
        try:
            file_size = os.path.getsize(output_file) / (1024 * 1024)  # MB
            last_modified = datetime.fromtimestamp(os.path.getmtime(output_file))
            
            scf_steps = 0
            geo_steps = 0
            current_energy = None
            converged = False
            
            with open(output_file, 'r') as f:
                content = f.read()
                
                # Count SCF steps
                scf_steps = len(re.findall(r'SCF run converged', content))
                
                # Count geometry optimization steps
                geo_steps = len(re.findall(r'STEP NUMBER\s+(\d+)', content))
                
                # Get latest energy
                energy_matches = re.findall(r'ENERGY\|\s+Total FORCE_EVAL.*?energy.*?:\s*([-\d\.]+)', content)
                if energy_matches:
                    current_energy = float(energy_matches[-1])
                
                # Check convergence
                if 'GEOMETRY OPTIMIZATION COMPLETED' in content:
                    converged = True
                elif 'MAXIMUM NUMBER OF OPTIMIZATION STEPS REACHED' in content:
                    converged = False
                
            return {
                'exists': True,
                'size_mb': file_size,
                'scf_steps': scf_steps,
                'geo_steps': geo_steps,
                'current_energy': current_energy,
                'converged': converged,
                'last_update': last_modified
            }
            
        except Exception as e:
            print(f"Error analyzing {output_file}: {e}")
            return {'exists': True, 'error': str(e)}

    def find_job_files(self, directory):
        """Find all job-related files in a directory"""
        job_files = {
            'slurm_script': None,
            'slurm_output': None,
            'slurm_error': None,
            'cp2k_input': None,
            'cp2k_output': None,
            'job_id': None
        }
        
        if not os.path.exists(directory):
            return job_files
        
        for file in os.listdir(directory):
            file_path = os.path.join(directory, file)
            
            if file.endswith('.slurm'):
                job_files['slurm_script'] = file_path
            elif file.endswith('.inp'):
                job_files['cp2k_input'] = file_path
            elif re.match(r'.*_(\d+)\.out$', file):
                job_files['slurm_output'] = file_path
                # Extract job ID
                match = re.search(r'_(\d+)\.out$', file)
                if match:
                    job_files['job_id'] = match.group(1)
            elif re.match(r'.*_(\d+)\.err$', file):
                job_files['slurm_error'] = file_path
            elif file.endswith('.out') and not re.match(r'.*_\d+\.out$', file):
                job_files['cp2k_output'] = file_path
        
        return job_files

    def calculate_cpu_hours(self, elapsed_minutes, ncpus):
        """Calculate CPU hours from elapsed time and number of CPUs"""
        if elapsed_minutes and ncpus:
            try:
                cpu_hours = (elapsed_minutes / 60.0) * int(ncpus)
                return cpu_hours
            except:
                return 0
        return 0

    def monitor_job_directory(self, directory):
        """Monitor a single job directory"""
        print(f"\n{'='*60}")
        print(f"MONITORING: {directory}")
        print(f"{'='*60}")
        
        job_files = self.find_job_files(directory)
        
        if not job_files['job_id']:
            print("❌ No job ID found - directory may not contain a submitted job")
            return
        
        job_id = job_files['job_id']
        print(f"🆔 Job ID: {job_id}")
        
        # Get current job status from SLURM
        job_info = self.get_job_info_from_squeue(job_id)
        if job_info:
            job = job_info[0]
            print(f"📊 Job Status: {job['status']}")
            print(f"⏱️  Time Elapsed: {job['time_elapsed']}")
            print(f"🖥️  Node(s): {job['node_list']}")
            
            # Calculate CPU hours for running job
            elapsed_minutes = self.parse_slurm_time(job['time_elapsed'])
            
            # Get number of CPUs from SLURM script or default to 8
            ncpus = 8  # Default based on our job setup
            if job_files['slurm_script']:
                try:
                    with open(job_files['slurm_script'], 'r') as f:
                        content = f.read()
                        match = re.search(r'#SBATCH --ntasks=(\d+)', content)
                        if match:
                            ncpus = int(match.group(1))
                except:
                    pass
            
            cpu_hours = self.calculate_cpu_hours(elapsed_minutes, ncpus)
            print(f"💻 CPU Hours Used: {cpu_hours:.2f} hours ({ncpus} cores × {elapsed_minutes/60:.2f} hours)")
            print(f"💰 Estimated Cost: ${cpu_hours * 0.10:.2f} (assuming $0.10/CPU-hour)")
            
        else:
            # Job not in queue, check if completed
            detailed_info = self.get_slurm_job_details(job_id)
            if detailed_info:
                print(f"📊 Job Status: {detailed_info['state']} (Completed)")
                print(f"⏱️  Total Runtime: {detailed_info['elapsed']}")
                print(f"🖥️  CPUs Used: {detailed_info['ncpus']}")
                
                elapsed_minutes = self.parse_slurm_time(detailed_info['elapsed'])
                cpu_hours = self.calculate_cpu_hours(elapsed_minutes, detailed_info['ncpus'])
                print(f"💻 Total CPU Hours: {cpu_hours:.2f} hours")
                print(f"💰 Total Cost: ${cpu_hours * 0.10:.2f}")
            else:
                print("❓ Job status unknown - may be too old or not found")
        
        # Analyze CP2K output if available
        if job_files['cp2k_output']:
            print(f"\n📄 CP2K Output Analysis:")
            analysis = self.analyze_cp2k_output(job_files['cp2k_output'])
            if analysis['exists']:
                print(f"   📊 File Size: {analysis['size_mb']:.2f} MB")
                print(f"   🔄 SCF Cycles: {analysis['scf_steps']}")
                print(f"   📐 Geometry Steps: {analysis['geo_steps']}")
                if analysis['current_energy']:
                    print(f"   ⚡ Current Energy: {analysis['current_energy']:.6f} Hartree")
                if analysis['converged']:
                    print(f"   ✅ Status: CONVERGED")
                else:
                    print(f"   🔄 Status: Running/In Progress")
                if analysis['last_update']:
                    print(f"   🕐 Last Update: {analysis['last_update'].strftime('%Y-%m-%d %H:%M:%S')}")
        else:
            print(f"\n📄 CP2K Output: Not yet available")
        
        # Check SLURM output for any errors or messages
        if job_files['slurm_output'] and os.path.exists(job_files['slurm_output']):
            try:
                with open(job_files['slurm_output'], 'r') as f:
                    slurm_content = f.read().strip()
                    if slurm_content:
                        print(f"\n📝 SLURM Output Messages:")
                        print(f"   {slurm_content}")
            except:
                pass

    def monitor_all_jobs(self, base_directory="energy_compare"):
        """Monitor all jobs in the energy_compare directory"""
        print(f"🔍 Scanning for CP2K jobs in {base_directory}/")
        
        if not os.path.exists(base_directory):
            print(f"❌ Directory {base_directory} not found")
            return
        
        job_dirs = []
        for item in os.listdir(base_directory):
            item_path = os.path.join(base_directory, item)
            if os.path.isdir(item_path):
                job_files = self.find_job_files(item_path)
                if job_files['job_id']:  # Has a job
                    job_dirs.append(item_path)
        
        if not job_dirs:
            print("❌ No CP2K jobs found")
            return
        
        print(f"✅ Found {len(job_dirs)} job directories")
        
        total_cpu_hours = 0
        for job_dir in job_dirs:
            self.monitor_job_directory(job_dir)
            
            # Add to total CPU hours calculation
            job_files = self.find_job_files(job_dir)
            if job_files['job_id']:
                job_id = job_files['job_id']
                job_info = self.get_job_info_from_squeue(job_id)
                if job_info:
                    job = job_info[0]
                    elapsed_minutes = self.parse_slurm_time(job['time_elapsed'])
                    ncpus = 8  # Default
                    cpu_hours = self.calculate_cpu_hours(elapsed_minutes, ncpus)
                    total_cpu_hours += cpu_hours
                else:
                    detailed_info = self.get_slurm_job_details(job_id)
                    if detailed_info:
                        elapsed_minutes = self.parse_slurm_time(detailed_info['elapsed'])
                        cpu_hours = self.calculate_cpu_hours(elapsed_minutes, detailed_info['ncpus'])
                        total_cpu_hours += cpu_hours
        
        print(f"\n{'='*60}")
        print(f"📊 TOTAL RESOURCE USAGE SUMMARY")
        print(f"{'='*60}")
        print(f"💻 Total CPU Hours: {total_cpu_hours:.2f} hours")
        print(f"💰 Total Estimated Cost: ${total_cpu_hours * 0.10:.2f}")
        print(f"🔬 Number of Jobs: {len(job_dirs)}")

def main():
    parser = argparse.ArgumentParser(description='Monitor CP2K job progress and calculate CPU hours')
    parser.add_argument('directory', nargs='?', help='Specific job directory to monitor')
    parser.add_argument('--all-jobs', action='store_true', help='Monitor all jobs in energy_compare/')
    parser.add_argument('--base-dir', default='energy_compare', help='Base directory to search for jobs')
    
    args = parser.parse_args()
    
    monitor = CP2KProgressMonitor()
    
    if args.all_jobs or not args.directory:
        monitor.monitor_all_jobs(args.base_dir)
    else:
        if os.path.exists(args.directory):
            monitor.monitor_job_directory(args.directory)
        else:
            print(f"❌ Directory {args.directory} not found")

if __name__ == "__main__":
    main() 
"""
Command-line interface for cp2k_slurm.

Provides commands for submitting and monitoring CP2K jobs on SLURM.
"""

import argparse
import sys
import time
from pathlib import Path
from typing import Optional

from .job_manager import JobManager
from .profiles import get_builtin_profiles, list_profiles


def cmd_submit(args):
    """Submit a CP2K job."""
    manager = JobManager(work_dir=args.work_dir)
    
    # Check if input file exists
    input_file = Path(args.input_file)
    if not input_file.exists():
        print(f"Error: Input file not found: {input_file}")
        return 1
    
    try:
        job_id = manager.submit(
            input_obj=input_file,
            profile=args.profile,
            job_name=args.name,
            time=args.time,
            nodes=args.nodes,
            ntasks_per_node=args.tasks_per_node,
            memory=args.memory
        )
        
        if args.wait:
            print(f"Waiting for job {job_id} to complete...")
            final_state = manager.wait(job_id, poll_interval=args.poll_interval)
            print(f"Job {job_id} finished with state: {final_state}")
            return 0 if final_state == "COMPLETED" else 1
        
        return 0
        
    except Exception as e:
        print(f"Error submitting job: {e}")
        return 1


def cmd_monitor(args):
    """Monitor a SLURM job."""
    manager = JobManager()
    
    try:
        if args.wait:
            final_state = manager.wait(args.job_id, poll_interval=args.poll_interval)
            print(f"Job {args.job_id} finished with state: {final_state}")
            return 0 if final_state == "COMPLETED" else 1
        else:
            # Just get current state
            state = manager.get_job_state(args.job_id)
            print(f"Job {args.job_id} state: {state}")
            return 0
            
    except Exception as e:
        print(f"Error monitoring job: {e}")
        return 1


def cmd_cancel(args):
    """Cancel a SLURM job."""
    manager = JobManager()
    
    try:
        success = manager.cancel_job(args.job_id)
        if success:
            print(f"Job {args.job_id} cancelled successfully")
            return 0
        else:
            print(f"Failed to cancel job {args.job_id}")
            return 1
            
    except Exception as e:
        print(f"Error cancelling job: {e}")
        return 1


def cmd_list(args):
    """List SLURM jobs."""
    manager = JobManager()
    
    try:
        jobs = manager.list_jobs(user=args.user)
        
        if not jobs:
            print("No jobs found")
            return 0
        
        # Print header
        print(f"{'JOB ID':<8} {'NAME':<20} {'STATE':<12} {'TIME':<10} {'NODES':<5} {'CPUS':<5}")
        print("-" * 70)
        
        # Print jobs
        for job in jobs:
            print(f"{job['job_id']:<8} {job['name']:<20} {job['state']:<12} "
                  f"{job['time']:<10} {job['nodes']:<5} {job['cpus']:<5}")
        
        return 0
        
    except Exception as e:
        print(f"Error listing jobs: {e}")
        return 1


def cmd_profiles(args):
    """List available resource profiles."""
    list_profiles()
    return 0


def cmd_info(args):
    """Get detailed job information."""
    manager = JobManager()
    
    try:
        info = manager.get_job_info(args.job_id)
        
        if 'error' in info:
            print(f"Error: {info['error']}")
            return 1
        
        print(f"Job Information for {args.job_id}:")
        print("-" * 40)
        
        # Print key information
        key_fields = ['jobid', 'jobname', 'jobstate', 'partition', 'nodes', 
                     'ntasks', 'cpus', 'submittime', 'starttime', 'endtime', 
                     'timelimit', 'workdir']
        
        for field in key_fields:
            if field in info:
                print(f"{field.capitalize():<12}: {info[field]}")
        
        return 0
        
    except Exception as e:
        print(f"Error getting job info: {e}")
        return 1


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="CP2K-SLURM job management tool",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Submit command
    submit_parser = subparsers.add_parser('submit', help='Submit a CP2K job')
    submit_parser.add_argument('input_file', help='CP2K input file')
    submit_parser.add_argument('--profile', '-p', default='short',
                              help='Resource profile (default: short)')
    submit_parser.add_argument('--name', '-n', help='Job name')
    submit_parser.add_argument('--work-dir', '-w', type=Path,
                              help='Working directory for job files')
    submit_parser.add_argument('--time', '-t', help='Time limit (e.g., 4:00:00)')
    submit_parser.add_argument('--nodes', type=int, help='Number of nodes')
    submit_parser.add_argument('--tasks-per-node', type=int, help='Tasks per node')
    submit_parser.add_argument('--memory', help='Memory limit (e.g., 16GB)')
    submit_parser.add_argument('--wait', action='store_true',
                              help='Wait for job completion')
    submit_parser.add_argument('--poll-interval', type=int, default=30,
                              help='Polling interval in seconds (default: 30)')
    submit_parser.set_defaults(func=cmd_submit)
    
    # Monitor command
    monitor_parser = subparsers.add_parser('monitor', help='Monitor a job')
    monitor_parser.add_argument('job_id', type=int, help='SLURM job ID')
    monitor_parser.add_argument('--wait', action='store_true',
                               help='Wait for job completion')
    monitor_parser.add_argument('--poll-interval', type=int, default=30,
                               help='Polling interval in seconds (default: 30)')
    monitor_parser.set_defaults(func=cmd_monitor)
    
    # Cancel command
    cancel_parser = subparsers.add_parser('cancel', help='Cancel a job')
    cancel_parser.add_argument('job_id', type=int, help='SLURM job ID')
    cancel_parser.set_defaults(func=cmd_cancel)
    
    # List command
    list_parser = subparsers.add_parser('list', help='List jobs')
    list_parser.add_argument('--user', '-u', help='Filter by user')
    list_parser.set_defaults(func=cmd_list)
    
    # Profiles command
    profiles_parser = subparsers.add_parser('profiles', help='List resource profiles')
    profiles_parser.set_defaults(func=cmd_profiles)
    
    # Info command
    info_parser = subparsers.add_parser('info', help='Get job information')
    info_parser.add_argument('job_id', type=int, help='SLURM job ID')
    info_parser.set_defaults(func=cmd_info)
    
    # Parse arguments
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    # Execute command
    return args.func(args)


if __name__ == '__main__':
    sys.exit(main()) 
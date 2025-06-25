"""
Job manager for CP2K-SLURM integration.

Handles job submission, monitoring, and management using subprocess calls
since pyslurm may not be available or compatible.
"""

import os
import subprocess
import time
import tempfile
from pathlib import Path
from typing import Union, Optional, Dict, Any, List, Callable
from dataclasses import dataclass
import re
import shutil

from jinja2 import Template, Environment, FileSystemLoader

from .profiles import ResourceProfile, get_profile


@dataclass
class JobStatus:
    """Job status information."""
    job_id: int
    state: str
    reason: Optional[str] = None
    runtime: Optional[str] = None
    nodes: Optional[str] = None
    exit_code: Optional[int] = None


class JobManager:
    """Manages CP2K job submission and monitoring on SLURM."""
    
    def __init__(self, work_dir: Optional[Path] = None):
        """
        Initialize JobManager.
        
        Args:
            work_dir: Working directory for jobs (default: current directory)
        """
        self.work_dir = Path(work_dir) if work_dir else Path.cwd()
        self.work_dir.mkdir(parents=True, exist_ok=True)
        
        # Get template directory
        template_dir = Path(__file__).parent / "templates"
        self.jinja_env = Environment(
            loader=FileSystemLoader(str(template_dir)),
            trim_blocks=True,
            lstrip_blocks=True
        )
    
    def submit(
        self,
        input_obj: Union[str, Path, Any],  # pycp2k.CP2K object or file path
        profile: Union[str, ResourceProfile] = "short",
        job_name: Optional[str] = None,
        output_name: Optional[str] = None,
        modules: Optional[List[str]] = None,
        **overrides
    ) -> int:
        """
        Submit a CP2K job to SLURM.
        
        Args:
            input_obj: CP2K input (pycp2k object, file path, or string)
            profile: Resource profile name or ResourceProfile object
            job_name: Custom job name
            output_name: Custom output file name
            modules: List of modules to load
            **overrides: Override profile parameters
            
        Returns:
            SLURM job ID
        """
        # Get or create resource profile
        if isinstance(profile, str):
            res_profile = get_profile(profile)
        else:
            res_profile = profile
        
        # Apply overrides
        if overrides:
            profile_dict = res_profile.__dict__.copy()
            profile_dict.update(overrides)
            res_profile = ResourceProfile(**profile_dict)
        
        # Handle input file
        input_path = self._prepare_input_file(input_obj, job_name)
        
        # Generate names
        if not job_name:
            job_name = res_profile.job_name or f"cp2k_{input_path.stem}"
        
        if not output_name:
            output_name = f"{input_path.stem}.out"
        
        # Create batch script
        script_path = self._create_batch_script(
            res_profile, input_path, output_name, job_name, modules
        )
        
        # Submit job
        job_id = self._submit_batch_script(script_path)
        
        print(f"Submitted CP2K job {job_id}: {job_name}")
        print(f"Input: {input_path}")
        print(f"Output: {output_name}")
        print(f"Script: {script_path}")
        
        return job_id
    
    def wait(
        self,
        job_id: int,
        poll_interval: int = 30,
        callbacks: Optional[Dict[str, Callable]] = None,
        timeout: Optional[int] = None
    ) -> JobStatus:
        """
        Wait for job completion with optional callbacks.
        
        Args:
            job_id: SLURM job ID
            poll_interval: Polling interval in seconds
            callbacks: State change callbacks {state: callable}
            timeout: Maximum wait time in seconds
            
        Returns:
            Final job status
        """
        start_time = time.time()
        last_state = None
        
        while True:
            status = self.get_job_status(job_id)
            
            if status is None:
                # Job not found, might have completed and been purged
                print(f"Job {job_id} not found in queue (may have completed)")
                break
            
            # Check for state change
            if status.state != last_state:
                print(f"Job {job_id} state: {last_state} -> {status.state}")
                
                # Execute callback if provided
                if callbacks and status.state in callbacks:
                    try:
                        callbacks[status.state](status)
                    except Exception as e:
                        print(f"Callback error for state {status.state}: {e}")
                
                last_state = status.state
            
            # Check if job is finished
            if status.state in ['COMPLETED', 'FAILED', 'CANCELLED', 'TIMEOUT']:
                print(f"Job {job_id} finished with state: {status.state}")
                return status
            
            # Check timeout
            if timeout and (time.time() - start_time) > timeout:
                print(f"Timeout waiting for job {job_id}")
                return status
            
            time.sleep(poll_interval)
        
        return status
    
    def get_job_status(self, job_id: int) -> Optional[JobStatus]:
        """Get current job status."""
        try:
            # Try squeue first (for running jobs)
            result = subprocess.run(
                ['squeue', '-j', str(job_id), '--format=%i,%T,%r,%M,%N', '--noheader'],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, 
                universal_newlines=True, check=True
            )
            
            if result.stdout.strip():
                fields = result.stdout.strip().split(',')
                return JobStatus(
                    job_id=int(fields[0]),
                    state=fields[1],
                    reason=fields[2] if fields[2] != 'None' else None,
                    runtime=fields[3] if fields[3] != 'N/A' else None,
                    nodes=fields[4] if fields[4] != 'N/A' else None
                )
        except subprocess.CalledProcessError:
            pass
        
        try:
            # Try sacct for completed jobs
            result = subprocess.run(
                ['sacct', '-j', str(job_id), '--format=JobID,State,ExitCode,Elapsed,NodeList', 
                 '--noheader', '--parsable2'],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, 
                universal_newlines=True, check=True
            )
            
            if result.stdout.strip():
                lines = result.stdout.strip().split('\n')
                # Get the main job (not job steps)
                for line in lines:
                    if not '.' in line.split('|')[0]:  # Main job, not job step
                        fields = line.split('|')
                        exit_code_str = fields[2]
                        exit_code = None
                        if ':' in exit_code_str:
                            exit_code = int(exit_code_str.split(':')[0])
                        
                        return JobStatus(
                            job_id=int(fields[0]),
                            state=fields[1],
                            runtime=fields[3],
                            nodes=fields[4],
                            exit_code=exit_code
                        )
        except subprocess.CalledProcessError:
            pass
        
        return None
    
    def cancel_job(self, job_id: int) -> bool:
        """Cancel a SLURM job."""
        try:
            subprocess.run(['scancel', str(job_id)], check=True)
            print(f"Cancelled job {job_id}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Failed to cancel job {job_id}: {e}")
            return False
    
    def list_jobs(self, user: Optional[str] = None) -> List[JobStatus]:
        """List jobs for current or specified user."""
        cmd = ['squeue', '--format=%i,%T,%r,%M,%N', '--noheader']
        if user:
            cmd.extend(['-u', user])
        
        try:
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, 
                                   universal_newlines=True, check=True)
            jobs = []
            
            for line in result.stdout.strip().split('\n'):
                if line.strip():
                    fields = line.split(',')
                    jobs.append(JobStatus(
                        job_id=int(fields[0]),
                        state=fields[1],
                        reason=fields[2] if fields[2] != 'None' else None,
                        runtime=fields[3] if fields[3] != 'N/A' else None,
                        nodes=fields[4] if fields[4] != 'N/A' else None
                    ))
            
            return jobs
        except subprocess.CalledProcessError:
            return []
    
    def _prepare_input_file(self, input_obj: Union[str, Path, Any], job_name: Optional[str] = None) -> Path:
        """Prepare CP2K input file."""
        if isinstance(input_obj, Path):
            # It's a Path object
            if not input_obj.exists():
                raise FileNotFoundError(f"Input file not found: {input_obj}")
            return input_obj.resolve()
        elif isinstance(input_obj, str):
            # Check if it's a file path or content
            if len(input_obj) < 260 and not '\n' in input_obj and Path(input_obj).exists():
                # Looks like a file path
                return Path(input_obj).resolve()
            else:
                # Treat as content string
                if job_name:
                    filename = f"{job_name}.inp"
                else:
                    filename = f"cp2k_input_{int(time.time())}.inp"
                input_path = self.work_dir / filename
                with open(input_path, 'w') as f:
                    f.write(input_obj)
                return input_path
        else:
            # Assume it's a pycp2k object or similar
            try:
                if job_name:
                    filename = f"{job_name}.inp"
                else:
                    filename = f"cp2k_input_{int(time.time())}.inp"
                input_path = self.work_dir / filename
                with open(input_path, 'w') as f:
                    f.write(str(input_obj))
                return input_path
            except Exception as e:
                raise ValueError(f"Could not convert input object to file: {e}")
    
    def _create_batch_script(
        self,
        profile: ResourceProfile,
        input_path: Path,
        output_name: str,
        job_name: str,
        modules: Optional[List[str]] = None
    ) -> Path:
        """Create SLURM batch script from template."""
        template = self.jinja_env.get_template('run.sh.j2')
        
        # Prepare template variables
        template_vars = {
            'job_name': job_name,
            'input_name': input_path.name,
            'output_name': output_name,
            'modules': modules,
            **profile.__dict__
        }
        
        # Render script
        script_content = template.render(**template_vars)
        
        # Write script file
        script_path = self.work_dir / f"{job_name}_{int(time.time())}.slurm"
        with open(script_path, 'w') as f:
            f.write(script_content)
        
        # Make executable
        script_path.chmod(0o755)
        
        return script_path
    
    def _submit_batch_script(self, script_path: Path) -> int:
        """Submit batch script and return job ID."""
        try:
            result = subprocess.run(
                ['sbatch', str(script_path)],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, 
                universal_newlines=True, check=True,
                cwd=self.work_dir
            )
            
            # Extract job ID from output like "Submitted batch job 12345"
            match = re.search(r'Submitted batch job (\d+)', result.stdout)
            if match:
                return int(match.group(1))
            else:
                raise RuntimeError(f"Could not parse job ID from: {result.stdout}")
                
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to submit job: {e.stderr}")


# Convenience functions
def submit_job(
    input_obj: Union[str, Path, Any],
    profile: Union[str, ResourceProfile] = "short",
    work_dir: Optional[Path] = None,
    **kwargs
) -> int:
    """Convenience function to submit a CP2K job."""
    manager = JobManager(work_dir)
    return manager.submit(input_obj, profile, **kwargs)


def wait_for_job(job_id: int, **kwargs) -> JobStatus:
    """Convenience function to wait for job completion."""
    manager = JobManager()
    return manager.wait(job_id, **kwargs) 
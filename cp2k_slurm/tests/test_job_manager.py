#!/usr/bin/env python3
"""
Tests for CP2K-SLURM job manager.

These tests verify the job submission and monitoring functionality.
"""

import os
import tempfile
import subprocess
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import pytest

from cp2k_slurm.job_manager import JobManager, JobStatus
from cp2k_slurm.profiles import ResourceProfile


class TestJobManager:
    """Test cases for JobManager class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.manager = JobManager(work_dir=self.temp_dir)
        
        # Sample CP2K input
        self.sample_input = """
&GLOBAL
  PROJECT_NAME test
  RUN_TYPE ENERGY
&END GLOBAL

&FORCE_EVAL
  METHOD Quickstep
  &DFT
    BASIS_SET_FILE_NAME BASIS_MOLOPT
    POTENTIAL_FILE_NAME GTH_POTENTIALS
    &SCF
      EPS_SCF 1.0E-6
    &END SCF
    &XC
      &XC_FUNCTIONAL PBE
      &END XC_FUNCTIONAL
    &END XC
  &END DFT
  &SUBSYS
    &CELL
      ABC 10.0 10.0 10.0
      PERIODIC NONE
    &END CELL
    &COORD
      H 0.0 0.0 0.0
      H 1.0 0.0 0.0
    &END COORD
    &KIND H
      BASIS_SET DZVP-MOLOPT-SR-GTH
      POTENTIAL GTH-PBE-q1
    &END KIND
  &END SUBSYS
&END FORCE_EVAL
"""
    
    def teardown_method(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_job_manager_initialization(self):
        """Test JobManager initialization."""
        assert self.manager.work_dir == self.temp_dir
        assert self.temp_dir.exists()
        assert hasattr(self.manager, 'jinja_env')
    
    def test_prepare_input_file_from_string(self):
        """Test preparing input file from string content."""
        input_path = self.manager._prepare_input_file(self.sample_input)
        
        assert input_path.exists()
        assert input_path.suffix == '.inp'
        assert self.sample_input.strip() in input_path.read_text()
    
    def test_prepare_input_file_from_path(self):
        """Test preparing input file from existing file path."""
        # Create test input file
        input_file = self.temp_dir / "test.inp"
        input_file.write_text(self.sample_input)
        
        input_path = self.manager._prepare_input_file(input_file)
        
        assert input_path == input_file.resolve()
        assert input_path.exists()
    
    def test_prepare_input_file_nonexistent(self):
        """Test error handling for non-existent input file."""
        nonexistent_file = self.temp_dir / "nonexistent.inp"
        
        with pytest.raises(FileNotFoundError):
            self.manager._prepare_input_file(nonexistent_file)
    
    @patch('subprocess.run')
    def test_create_batch_script(self, mock_run):
        """Test batch script creation."""
        profile = ResourceProfile(
            nodes=1,
            ntasks_per_node=8,
            cpus_per_task=1,
            time="04:00:00",
            job_name="test_job"
        )
        
        input_file = self.temp_dir / "test.inp"
        input_file.write_text(self.sample_input)
        
        script_path = self.manager._create_batch_script(
            profile, input_file, "test.out", "test_job", None
        )
        
        assert script_path.exists()
        assert script_path.suffix == '.slurm'
        
        script_content = script_path.read_text()
        assert "#SBATCH --job-name=test_job" in script_content
        assert "#SBATCH --nodes=1" in script_content
        assert "#SBATCH --ntasks-per-node=8" in script_content
        assert "#SBATCH --time=04:00:00" in script_content
        assert "cp2k.psmp -i test.inp -o test.out" in script_content
    
    @patch('subprocess.run')
    def test_submit_batch_script_success(self, mock_run):
        """Test successful batch script submission."""
        mock_run.return_value = Mock(
            stdout="Submitted batch job 12345\n",
            stderr="",
            returncode=0
        )
        
        script_path = self.temp_dir / "test.slurm"
        script_path.write_text("#!/bin/bash\necho test")
        
        job_id = self.manager._submit_batch_script(script_path)
        
        assert job_id == 12345
        mock_run.assert_called_once()
        args = mock_run.call_args[0][0]
        assert args[0] == 'sbatch'
        assert str(script_path) in args
    
    @patch('subprocess.run')
    def test_submit_batch_script_failure(self, mock_run):
        """Test batch script submission failure."""
        mock_run.side_effect = subprocess.CalledProcessError(
            1, ['sbatch'], stderr="Permission denied"
        )
        
        script_path = self.temp_dir / "test.slurm"
        script_path.write_text("#!/bin/bash\necho test")
        
        with pytest.raises(RuntimeError, match="Failed to submit job"):
            self.manager._submit_batch_script(script_path)
    
    @patch('subprocess.run')
    def test_get_job_status_running(self, mock_run):
        """Test getting status of running job."""
        mock_run.return_value = Mock(
            stdout="12345,RUNNING,None,10:30,node001\n",
            stderr="",
            returncode=0
        )
        
        status = self.manager.get_job_status(12345)
        
        assert status is not None
        assert status.job_id == 12345
        assert status.state == "RUNNING"
        assert status.runtime == "10:30"
        assert status.nodes == "node001"
    
    @patch('subprocess.run')
    def test_get_job_status_completed(self, mock_run):
        """Test getting status of completed job."""
        # First call (squeue) returns empty - job not in queue
        # Second call (sacct) returns completed job info
        mock_run.side_effect = [
            Mock(stdout="", stderr="", returncode=0),  # squeue
            Mock(stdout="12345|COMPLETED|0:0|15:45|node001\n", stderr="", returncode=0)  # sacct
        ]
        
        status = self.manager.get_job_status(12345)
        
        assert status is not None
        assert status.job_id == 12345
        assert status.state == "COMPLETED"
        assert status.exit_code == 0
        assert status.runtime == "15:45"
    
    @patch('subprocess.run')
    def test_get_job_status_not_found(self, mock_run):
        """Test getting status of non-existent job."""
        mock_run.side_effect = [
            subprocess.CalledProcessError(1, ['squeue']),  # squeue fails
            subprocess.CalledProcessError(1, ['sacct'])    # sacct fails
        ]
        
        status = self.manager.get_job_status(12345)
        
        assert status is None
    
    @patch('subprocess.run')
    def test_cancel_job_success(self, mock_run):
        """Test successful job cancellation."""
        mock_run.return_value = Mock(returncode=0)
        
        result = self.manager.cancel_job(12345)
        
        assert result is True
        mock_run.assert_called_once_with(['scancel', '12345'], check=True)
    
    @patch('subprocess.run')
    def test_cancel_job_failure(self, mock_run):
        """Test job cancellation failure."""
        mock_run.side_effect = subprocess.CalledProcessError(1, ['scancel'])
        
        result = self.manager.cancel_job(12345)
        
        assert result is False
    
    @patch('subprocess.run')
    def test_list_jobs(self, mock_run):
        """Test listing jobs."""
        mock_run.return_value = Mock(
            stdout="12345,RUNNING,None,10:30,node001\n12346,PENDING,Resources,0:00,N/A\n",
            stderr="",
            returncode=0
        )
        
        jobs = self.manager.list_jobs()
        
        assert len(jobs) == 2
        assert jobs[0].job_id == 12345
        assert jobs[0].state == "RUNNING"
        assert jobs[1].job_id == 12346
        assert jobs[1].state == "PENDING"
        assert jobs[1].reason == "Resources"
    
    @patch('cp2k_slurm.job_manager.JobManager._submit_batch_script')
    @patch('cp2k_slurm.job_manager.JobManager._create_batch_script')
    @patch('cp2k_slurm.job_manager.JobManager._prepare_input_file')
    def test_submit_integration(self, mock_prepare, mock_create, mock_submit):
        """Test full submit workflow integration."""
        # Setup mocks
        input_file = self.temp_dir / "test.inp"
        script_file = self.temp_dir / "test.slurm"
        
        mock_prepare.return_value = input_file
        mock_create.return_value = script_file
        mock_submit.return_value = 12345
        
        # Create actual input file for the test
        input_file.write_text(self.sample_input)
        
        # Submit job
        job_id = self.manager.submit(
            input_obj=self.sample_input,
            profile="short",
            job_name="test_integration"
        )
        
        assert job_id == 12345
        mock_prepare.assert_called_once()
        mock_create.assert_called_once()
        mock_submit.assert_called_once()


class TestJobStatus:
    """Test cases for JobStatus dataclass."""
    
    def test_job_status_creation(self):
        """Test JobStatus creation."""
        status = JobStatus(
            job_id=12345,
            state="RUNNING",
            reason=None,
            runtime="10:30",
            nodes="node001"
        )
        
        assert status.job_id == 12345
        assert status.state == "RUNNING"
        assert status.runtime == "10:30"
        assert status.nodes == "node001"
        assert status.exit_code is None


@pytest.mark.slurm
class TestSlurmIntegration:
    """Integration tests that require actual SLURM installation."""
    
    def test_slurm_version_check(self):
        """Test that SLURM version can be detected."""
        try:
            result = subprocess.run(
                ['sinfo', '--version'],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, 
                universal_newlines=True, check=True
            )
            assert 'slurm' in result.stdout.lower()
            # Should contain version like "22.05"
            assert any(char.isdigit() for char in result.stdout)
        except (subprocess.CalledProcessError, FileNotFoundError):
            pytest.skip("SLURM not available")
    
    def test_slurm_commands_available(self):
        """Test that required SLURM commands are available."""
        commands = ['sbatch', 'squeue', 'sacct', 'scancel']
        
        for cmd in commands:
            try:
                result = subprocess.run(
                    ['which', cmd],
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, 
                    check=True
                )
                assert result.returncode == 0
            except subprocess.CalledProcessError:
                pytest.skip(f"SLURM command {cmd} not available")


if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 
"""
CP2K-SLURM Integration Package

A Python package for submitting and monitoring CP2K jobs on SLURM clusters.
Adapted for CP2K 2023.1 with Intel MPI and SLURM 22.05.8.
"""

__version__ = "0.1.0"
__author__ = "PyCP2K SLURM Integration"

import sys
import subprocess
from pathlib import Path

def _check_slurm_version():
    """Check SLURM version compatibility"""
    try:
        result = subprocess.run(['sinfo', '--version'], 
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, 
                              universal_newlines=True)
        if result.returncode == 0:
            version_line = result.stdout.strip()
            if "22.05" in version_line:
                return True
            else:
                print(f"Warning: cp2k_slurm tested with SLURM 22.05.x, found: {version_line}")
                return True  # Allow but warn
        return False
    except (OSError, FileNotFoundError):
        print("Warning: Could not verify SLURM version")
        return True  # Allow if can't check

def _check_cp2k_availability():
    """Check CP2K executable availability"""
    try:
        # Check for cp2k.popt (used in your environment)
        result = subprocess.run(['which', 'cp2k.popt'], 
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                              universal_newlines=True)
        if result.returncode == 0:
            return True
        
        # Fallback to cp2k.psmp
        result = subprocess.run(['which', 'cp2k.psmp'], 
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                              universal_newlines=True)
        return result.returncode == 0
    except (OSError, FileNotFoundError):
        return False

# Perform compatibility checks
if not _check_slurm_version():
    print("Warning: SLURM version check failed")

if not _check_cp2k_availability():
    print("Warning: CP2K executable not found in PATH")

# Import main components
from .job_manager import JobManager
from .profiles import ResourceProfile, get_builtin_profiles

__all__ = ['JobManager', 'ResourceProfile', 'get_builtin_profiles'] 
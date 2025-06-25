#!/usr/bin/env python3
"""
Simple test script to verify cp2k_slurm package functionality.
"""

import sys
from pathlib import Path

# Add package to path
sys.path.insert(0, str(Path(__file__).parent.parent))

def test_imports():
    """Test that all modules can be imported."""
    try:
        import cp2k_slurm
        from cp2k_slurm import JobManager, ResourceProfile, get_builtin_profiles
        from cp2k_slurm.job_manager import JobStatus
        from cp2k_slurm.profiles import get_profile
        print("✓ All imports successful")
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False

def test_profiles():
    """Test profile functionality."""
    try:
        from cp2k_slurm import get_builtin_profiles, ResourceProfile
        from cp2k_slurm.profiles import get_profile
        
        profiles = get_builtin_profiles()
        print(f"✓ Found {len(profiles)} built-in profiles")
        
        # Test getting a specific profile
        short_profile = get_profile("short")
        print(f"✓ Short profile: {short_profile.nodes}n × {short_profile.ntasks_per_node}t")
        
        # Test custom profile
        custom = ResourceProfile(nodes=2, ntasks_per_node=8, time="12:00:00")
        print(f"✓ Custom profile: {custom.total_mpi_tasks} total MPI tasks")
        
        return True
    except Exception as e:
        print(f"✗ Profile error: {e}")
        return False

def test_job_manager():
    """Test JobManager initialization."""
    try:
        import tempfile
        from cp2k_slurm import JobManager
        
        with tempfile.TemporaryDirectory() as temp_dir:
            manager = JobManager(work_dir=temp_dir)
            print(f"✓ JobManager created with work_dir: {manager.work_dir}")
            
            # Test template environment
            template = manager.jinja_env.get_template('run.sh.j2')
            print("✓ Template system working")
            
        return True
    except Exception as e:
        print(f"✗ JobManager error: {e}")
        return False

def test_cli_imports():
    """Test CLI imports (optional)."""
    try:
        from cp2k_slurm.cli import app
        print("✓ CLI imports successful")
        return True
    except ImportError as e:
        print(f"⚠ CLI imports failed (optional): {e}")
        return True  # CLI is optional

def main():
    """Run all tests."""
    print("Testing cp2k_slurm package...")
    print("=" * 40)
    
    tests = [
        test_imports,
        test_profiles,
        test_job_manager,
        test_cli_imports
    ]
    
    results = []
    for test in tests:
        print(f"\nRunning {test.__name__}...")
        results.append(test())
    
    print("\n" + "=" * 40)
    passed = sum(results)
    total = len(results)
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("✓ All tests passed! Package is ready to use.")
        return 0
    else:
        print("✗ Some tests failed. Check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 
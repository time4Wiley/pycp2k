# CP2K-SLURM Integration Package

A Python package for seamless integration between CP2K quantum chemistry calculations and SLURM workload manager on HPC clusters.

## Features

- **Easy Job Submission**: Submit CP2K jobs with predefined or custom resource profiles
- **Job Monitoring**: Real-time job status monitoring with rich terminal output
- **Resource Profiles**: Predefined configurations for common CP2K workloads
- **CLI Interface**: Command-line tools for job management
- **Template System**: Flexible SLURM batch script generation
- **Error Handling**: Robust error detection and reporting
- **CP2K Integration**: Works with pycp2k objects and input files

## Installation

### Basic Installation

```bash
pip install cp2k_slurm
```

### With CLI Support

```bash
pip install cp2k_slurm[cli]
```

### With PyCP2K Integration

```bash
pip install cp2k_slurm[pycp2k]
```

### Development Installation

```bash
git clone https://github.com/your-org/cp2k_slurm.git
cd cp2k_slurm
pip install -e .[all]
```

## Quick Start

### Python API

```python
from cp2k_slurm import JobManager

# Create job manager
manager = JobManager(work_dir="./my_calculations")

# Submit a job with built-in profile
job_id = manager.submit(
    input_obj="water.inp",
    profile="short",
    job_name="water_optimization"
)

print(f"Submitted job {job_id}")

# Monitor job completion
final_status = manager.wait(job_id, poll_interval=30)
print(f"Job completed with status: {final_status.state}")
```

### Command Line Interface

```bash
# Submit a job
cp2k_slurm submit water.inp --profile short --name water_opt

# Watch job progress
cp2k_slurm watch 12345 --follow

# List all jobs
cp2k_slurm list

# Show available profiles
cp2k_slurm profiles

# Cancel a job
cp2k_slurm cancel 12345
```

## Resource Profiles

Built-in profiles optimized for common CP2K workloads:

| Profile | Nodes | Tasks/Node | CPUs/Task | Time | Memory | Use Case |
|---------|-------|------------|-----------|------|---------|----------|
| `short` | 1 | 8 | 1 | 4h | 4G/CPU | Quick calculations |
| `medium` | 1 | 16 | 1 | 12h | 4G/CPU | Standard DFT |
| `long` | 1 | 8 | 1 | 24h | 6G/CPU | Long optimizations |
| `geo_opt` | 1 | 8 | 1 | 6h | 4G/CPU | Geometry optimization |
| `multinode` | 2 | 16 | 1 | 12h | 4G/CPU | Large systems |
| `gpu_small` | 1 | 4 | 2 | 8h | 8G/CPU | GPU calculations |
| `memory_intensive` | 1 | 8 | 2 | 16h | 128G/node | High memory needs |

### Custom Profiles

```python
from cp2k_slurm import ResourceProfile

# Create custom profile
custom_profile = ResourceProfile(
    nodes=2,
    ntasks_per_node=16,
    cpus_per_task=1,
    time="24:00:00",
    mem_per_cpu="8G",
    partition="gpu",
    gres="gpu:2"
)

# Use custom profile
job_id = manager.submit("input.inp", profile=custom_profile)
```

## Environment Setup

### HPC Module Loading

The package automatically loads required modules, but you can customize:

```python
job_id = manager.submit(
    "input.inp",
    profile="short",
    modules=["intel/2023.1", "intel-mpi/2021.9", "cp2k/2023.1"]
)
```

### Environment Variables

The package sets optimal MPI environment variables for Intel MPI:

```bash
export I_MPI_PMI_LIBRARY=/opt/gridview/slurm/lib/libpmi2.so
export I_MPI_PMI=pmi2
export I_MPI_FABRICS=shm:ofi
export I_MPI_OFI_PROVIDER=verbs
```

## Advanced Usage

### Job Callbacks

Monitor job state changes with callbacks:

```python
def on_running(status):
    print(f"Job started on nodes: {status.nodes}")

def on_completed(status):
    print(f"Job finished with exit code: {status.exit_code}")

callbacks = {
    'RUNNING': on_running,
    'COMPLETED': on_completed,
    'FAILED': lambda s: print("Job failed!")
}

final_status = manager.wait(job_id, callbacks=callbacks)
```

### PyCP2K Integration

```python
from pycp2k import CP2K

# Create CP2K input object
cp2k_input = CP2K()
cp2k_input.GLOBAL.PROJECT_NAME = "water"
cp2k_input.GLOBAL.RUN_TYPE = "GEO_OPT"
# ... configure input ...

# Submit directly
job_id = manager.submit(cp2k_input, profile="geo_opt")
```

### Profile Overrides

```python
# Override specific parameters
job_id = manager.submit(
    "input.inp",
    profile="short",
    time="8:00:00",        # Override time limit
    nodes=2,               # Override node count
    partition="gpu",       # Override partition
    account="my_project"   # Set account
)
```

## Configuration

### SLURM Compatibility

This package is designed for SLURM 22.05.x but should work with other versions. The package automatically detects SLURM version and warns about compatibility issues.

### CP2K Executables

The package looks for CP2K executables in this order:
1. `cp2k.psmp` (parallel, shared memory)
2. `cp2k.popt` (parallel, OpenMP)

You can specify the executable in profiles:

```python
profile = ResourceProfile(
    cp2k_executable="cp2k.psmp",
    mpi_command="mpirun"
)
```

## Error Handling

The package provides comprehensive error handling:

- **Input validation**: Checks for file existence and profile validity
- **SLURM errors**: Captures and reports SLURM command failures
- **Job monitoring**: Detects failed jobs and provides diagnostics
- **Resource checking**: Validates resource requests against limits

## Examples

### Geometry Optimization

```python
from cp2k_slurm import JobManager

manager = JobManager("./geometry_optimization")

# Submit geometry optimization
job_id = manager.submit(
    "molecule.inp",
    profile="geo_opt",
    job_name="mol_geometry",
    output_name="mol_geo.out"
)

# Wait for completion
status = manager.wait(job_id, timeout=3600)

if status.state == "COMPLETED":
    print("Geometry optimization completed successfully!")
else:
    print(f"Job failed with state: {status.state}")
```

### Batch Processing

```python
import os
from pathlib import Path

manager = JobManager("./batch_calculations")

# Submit multiple jobs
job_ids = []
for input_file in Path(".").glob("*.inp"):
    job_id = manager.submit(
        input_file,
        profile="short",
        job_name=f"calc_{input_file.stem}"
    )
    job_ids.append(job_id)

# Monitor all jobs
print(f"Submitted {len(job_ids)} jobs")
for job_id in job_ids:
    print(f"Job {job_id}: {manager.get_job_status(job_id).state}")
```

## Testing

Run the test suite:

```bash
# Basic tests (no SLURM required)
pytest tests/ -m "not slurm"

# Full tests (requires SLURM)
pytest tests/

# With coverage
pytest tests/ --cov=cp2k_slurm --cov-report=html
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

### Development Setup

```bash
git clone https://github.com/your-org/cp2k_slurm.git
cd cp2k_slurm
pip install -e .[dev]
pre-commit install
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

- **Issues**: Report bugs and feature requests on GitHub Issues
- **Documentation**: See the `examples/` directory for more examples
- **HPC Support**: Contact your HPC center for SLURM-specific issues

## Changelog

### v0.1.0
- Initial release
- Basic job submission and monitoring
- CLI interface
- Built-in resource profiles
- PyCP2K integration
- Comprehensive test suite

## Acknowledgments

- CP2K development team for the quantum chemistry package
- SchedMD for SLURM workload manager
- PyCP2K developers for the Python interface 
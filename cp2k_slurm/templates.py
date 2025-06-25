"""
SLURM script templates for CP2K jobs.

Provides Jinja2 templates and rendering functions for generating SLURM batch scripts.
"""

from typing import Dict, Any
from pathlib import Path

# Default SLURM script template adapted for your environment
DEFAULT_SLURM_TEMPLATE = """#!/bin/bash
#SBATCH --job-name={{ job_name }}
#SBATCH --output={{ job_name }}-%j.out
#SBATCH --error={{ job_name }}-%j.err
#SBATCH --time={{ time }}
#SBATCH --nodes={{ nodes }}
#SBATCH --ntasks-per-node={{ ntasks_per_node }}
#SBATCH --cpus-per-task={{ cpus_per_task }}
{%- if mem is defined %}
#SBATCH --mem={{ mem }}
{%- endif %}
{%- if partition is defined %}
#SBATCH --partition={{ partition }}
{%- endif %}
{%- if qos is defined %}
#SBATCH --qos={{ qos }}
{%- endif %}
{%- if account is defined %}
#SBATCH --account={{ account }}
{%- endif %}
{%- if gpus is defined %}
#SBATCH --gpus={{ gpus }}
{%- endif %}
{%- if gres is defined %}
#SBATCH --gres={{ gres }}
{%- endif %}

# Environment setup
module purge
module load cp2k/2023.1  # Adapted for your CP2K version
module load intel/2023.1.0  # Intel MPI based on your setup

# Set environment variables for Intel MPI (based on your working configuration)
export I_MPI_PMI_LIBRARY=/opt/gridview/slurm/lib/libpmi2.so
export I_MPI_PMI=pmi2
export I_MPI_FABRICS=shm:ofi
export I_MPI_OFI_PROVIDER=verbs

# Job information
echo "Job ID: $SLURM_JOB_ID"
echo "Job Name: {{ job_name }}"
echo "Node(s): $SLURM_JOB_NODELIST"
echo "Number of nodes: $SLURM_JOB_NUM_NODES"
echo "Number of tasks: $SLURM_NTASKS"
echo "CPUs per task: $SLURM_CPUS_PER_TASK"
echo "Working directory: $PWD"
echo "Started at: $(date)"

# CP2K execution
echo "Running CP2K with input: {{ input_file }}"
mpirun -np $SLURM_NTASKS {{ cp2k_executable }} -i {{ input_file }} -o {{ output_file }}

# Job completion
echo "Finished at: $(date)"
echo "Exit code: $?"
"""

# Template for GPU jobs
GPU_SLURM_TEMPLATE = """#!/bin/bash
#SBATCH --job-name={{ job_name }}
#SBATCH --output={{ job_name }}-%j.out
#SBATCH --error={{ job_name }}-%j.err
#SBATCH --time={{ time }}
#SBATCH --nodes={{ nodes }}
#SBATCH --ntasks-per-node={{ ntasks_per_node }}
#SBATCH --cpus-per-task={{ cpus_per_task }}
#SBATCH --gpus={{ gpus }}
#SBATCH --gres={{ gres }}
{%- if mem is defined %}
#SBATCH --mem={{ mem }}
{%- endif %}
{%- if partition is defined %}
#SBATCH --partition={{ partition }}
{%- endif %}
{%- if qos is defined %}
#SBATCH --qos={{ qos }}
{%- endif %}
{%- if account is defined %}
#SBATCH --account={{ account }}
{%- endif %}

# Environment setup
module purge
module load cp2k/2023.1-gpu  # GPU-enabled CP2K
module load intel/2023.1.0
module load cuda/11.8

# Set environment variables
export I_MPI_PMI_LIBRARY=/opt/gridview/slurm/lib/libpmi2.so
export I_MPI_PMI=pmi2
export I_MPI_FABRICS=shm:ofi
export I_MPI_OFI_PROVIDER=verbs

# GPU setup
export CUDA_VISIBLE_DEVICES=$SLURM_LOCALID

# Job information
echo "Job ID: $SLURM_JOB_ID"
echo "Job Name: {{ job_name }}"
echo "Node(s): $SLURM_JOB_NODELIST"
echo "Number of nodes: $SLURM_JOB_NUM_NODES"
echo "Number of tasks: $SLURM_NTASKS"
echo "CPUs per task: $SLURM_CPUS_PER_TASK"
echo "GPUs: {{ gpus }}"
echo "Working directory: $PWD"
echo "Started at: $(date)"

# CP2K execution
echo "Running CP2K with input: {{ input_file }}"
mpirun -np $SLURM_NTASKS {{ cp2k_executable }} -i {{ input_file }} -o {{ output_file }}

# Job completion
echo "Finished at: $(date)"
echo "Exit code: $?"
"""


def render_slurm_script(context: Dict[str, Any], 
                       template: str = None) -> str:
    """
    Render SLURM script from template and context.
    
    Args:
        context: Template variables
        template: Custom template string (uses default if None)
        
    Returns:
        Rendered SLURM script content
    """
    try:
        from jinja2 import Template
    except ImportError:
        # Fallback to simple string formatting if Jinja2 not available
        return _render_simple_template(context, template)
    
    # Choose template based on GPU usage
    if template is None:
        if context.get('gpus') or context.get('gres'):
            template = GPU_SLURM_TEMPLATE
        else:
            template = DEFAULT_SLURM_TEMPLATE
    
    jinja_template = Template(template)
    return jinja_template.render(**context)


def _render_simple_template(context: Dict[str, Any], 
                           template: str = None) -> str:
    """
    Simple template rendering without Jinja2 (fallback).
    
    This provides basic functionality if Jinja2 is not available.
    """
    if template is None:
        # Use simplified template without conditionals
        template = """#!/bin/bash
#SBATCH --job-name={job_name}
#SBATCH --output={job_name}-%j.out
#SBATCH --error={job_name}-%j.err
#SBATCH --time={time}
#SBATCH --nodes={nodes}
#SBATCH --ntasks-per-node={ntasks_per_node}
#SBATCH --cpus-per-task={cpus_per_task}

# Environment setup
module purge
module load cp2k/2023.1
module load intel/2023.1.0

# Set environment variables for Intel MPI
export I_MPI_PMI_LIBRARY=/opt/gridview/slurm/lib/libpmi2.so
export I_MPI_PMI=pmi2
export I_MPI_FABRICS=shm:ofi
export I_MPI_OFI_PROVIDER=verbs

# Job information
echo "Job ID: $SLURM_JOB_ID"
echo "Job Name: {job_name}"
echo "Started at: $(date)"

# CP2K execution
echo "Running CP2K with input: {input_file}"
mpirun -np $SLURM_NTASKS {cp2k_executable} -i {input_file} -o {output_file}

# Job completion
echo "Finished at: $(date)"
echo "Exit code: $?"
"""
    
    # Simple string formatting
    try:
        return template.format(**context)
    except KeyError as e:
        raise ValueError(f"Missing template variable: {e}")


def save_template(template_content: str, 
                 template_path: Path) -> None:
    """Save a custom template to file."""
    template_path.parent.mkdir(parents=True, exist_ok=True)
    template_path.write_text(template_content)


def load_template(template_path: Path) -> str:
    """Load a template from file."""
    if not template_path.exists():
        raise FileNotFoundError(f"Template not found: {template_path}")
    return template_path.read_text() 
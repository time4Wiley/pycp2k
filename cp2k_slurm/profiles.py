"""
Resource profiles for CP2K jobs on SLURM clusters.

Defines standard resource configurations for different types of CP2K calculations.
"""

from dataclasses import dataclass, field
from typing import Dict, Optional, Any


@dataclass
class ResourceProfile:
    """Resource profile for CP2K SLURM jobs."""
    
    nodes: int = 1
    ntasks_per_node: int = 8
    cpus_per_task: int = 1
    gpus: Optional[int] = None
    time: str = "4:00:00"
    partition: Optional[str] = None
    qos: Optional[str] = None
    gres: Optional[str] = None
    account: Optional[str] = None
    memory: Optional[str] = None
    extra_sbatch_opts: Dict[str, Any] = field(default_factory=dict)
    
    @property
    def total_cores(self) -> int:
        """Calculate total CPU cores requested."""
        return self.nodes * self.ntasks_per_node * self.cpus_per_task
    
    @property
    def total_mpi_tasks(self) -> int:
        """Calculate total MPI tasks."""
        return self.nodes * self.ntasks_per_node
    
    def to_sbatch_dict(self) -> Dict[str, Any]:
        """Convert profile to SBATCH parameters dictionary."""
        params = {
            'nodes': self.nodes,
            'ntasks-per-node': self.ntasks_per_node,
            'cpus-per-task': self.cpus_per_task,
            'time': self.time,
        }
        
        if self.gpus is not None:
            params['gpus'] = self.gpus
        if self.partition:
            params['partition'] = self.partition
        if self.qos:
            params['qos'] = self.qos
        if self.gres:
            params['gres'] = self.gres
        if self.account:
            params['account'] = self.account
        if self.memory:
            params['mem'] = self.memory
            
        # Add extra options
        params.update(self.extra_sbatch_opts)
        
        return params


# Built-in profiles adapted for your HPC environment
BUILTIN_PROFILES = {
    "quick": ResourceProfile(
        nodes=1,
        ntasks_per_node=4,
        cpus_per_task=1,
        time="1:00:00",
        memory="8GB"
    ),
    
    "short": ResourceProfile(
        nodes=1,
        ntasks_per_node=8,
        cpus_per_task=1,
        time="4:00:00",
        memory="16GB"
    ),
    
    "medium": ResourceProfile(
        nodes=1,
        ntasks_per_node=16,
        cpus_per_task=1,
        time="12:00:00",
        memory="32GB"
    ),
    
    "long": ResourceProfile(
        nodes=1,
        ntasks_per_node=8,
        cpus_per_task=1,
        time="24:00:00",
        memory="16GB"
    ),
    
    "multinode": ResourceProfile(
        nodes=2,
        ntasks_per_node=8,
        cpus_per_task=1,
        time="8:00:00",
        memory="16GB"
    ),
    
    "large_memory": ResourceProfile(
        nodes=1,
        ntasks_per_node=8,
        cpus_per_task=2,
        time="8:00:00",
        memory="64GB"
    ),
    
    # GPU profiles (if available)
    "gpu_small": ResourceProfile(
        nodes=1,
        ntasks_per_node=4,
        cpus_per_task=2,
        gpus=1,
        time="4:00:00",
        memory="16GB",
        gres="gpu:1"
    ),
    
    "gpu_large": ResourceProfile(
        nodes=1,
        ntasks_per_node=8,
        cpus_per_task=2,
        gpus=2,
        time="12:00:00",
        memory="32GB",
        gres="gpu:2"
    ),
}


def get_builtin_profiles() -> Dict[str, ResourceProfile]:
    """Get dictionary of built-in resource profiles."""
    return BUILTIN_PROFILES.copy()


def get_profile(name: str) -> ResourceProfile:
    """Get a built-in profile by name."""
    if name not in BUILTIN_PROFILES:
        available = ", ".join(BUILTIN_PROFILES.keys())
        raise ValueError(f"Unknown profile '{name}'. Available profiles: {available}")
    return BUILTIN_PROFILES[name]


def list_profiles() -> None:
    """Print available profiles with their configurations."""
    print("Available resource profiles:")
    print("-" * 50)
    
    for name, profile in BUILTIN_PROFILES.items():
        print(f"{name:12} | {profile.nodes:2}n × {profile.ntasks_per_node:2}t × {profile.cpus_per_task:1}c "
              f"| {profile.time:8} | {profile.memory or 'auto':>6}")
        if profile.gpus:
            print(f"             | GPUs: {profile.gpus}")
    
    print("-" * 50)
    print("Legend: n=nodes, t=tasks/node, c=cpus/task") 
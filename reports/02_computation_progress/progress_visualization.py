#!/usr/bin/env python3
"""
Progress Visualization for Geometry Optimization Computations
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

def create_simple_progress():
    """Create a simple progress visualization"""
    
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    
    # Simple progress data
    jobs = ['PVA-Borate\nJob 15269072', 'CBA-Borate\nJob 15269073']
    progress = [85, 80]  # Estimated progress percentage
    colors = ['green', 'blue']
    
    bars = ax.bar(jobs, progress, color=colors, alpha=0.7, edgecolor='black')
    
    # Add progress labels
    for bar, prog in zip(bars, progress):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{prog}%', ha='center', va='bottom', fontweight='bold')
    
    ax.set_ylabel('Estimated Progress (%)', fontsize=14, fontweight='bold')
    ax.set_title('Geometry Optimization Progress\nRunning for ~21 hours', fontsize=16, fontweight='bold')
    ax.set_ylim(0, 100)
    ax.grid(True, alpha=0.3, axis='y')
    
    # Add status info
    ax.text(0.5, 50, 'Both jobs actively running\non AMD EPYC compute nodes\nUsing CP2K 2023.1 + Intel MPI', 
           ha='center', va='center', fontsize=12, fontweight='bold',
           bbox=dict(boxstyle="round,pad=0.5", facecolor='lightyellow', alpha=0.8))
    
    plt.tight_layout()
    plt.savefig('progress_status.png', dpi=300, bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    print("Creating progress visualization...")
    create_simple_progress()
    print("Created progress_status.png") 
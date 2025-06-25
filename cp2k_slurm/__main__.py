#!/usr/bin/env python3
"""
Main entry point for cp2k_slurm package.

Allows running the CLI with: python -m cp2k_slurm
"""

import sys
from .cli import main

if __name__ == "__main__":
    sys.exit(main()) 
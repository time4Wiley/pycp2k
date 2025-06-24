#!/bin/bash

cd 01_pva_borate && sbatch job.slurm && cd ..
cd 02_cba_borate && sbatch job.slurm && cd .. 
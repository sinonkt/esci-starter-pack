#!/bin/bash
#SBATCH --partition=cpugpu
#SBATCH --qos=cu_hpc
#SBATCH --gpus=1
#SBATCH --cpus-per-task=2
#SBATCH --mem=8G

sleep 60
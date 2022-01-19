#!/bin/bash
#
#SBATCH --qos=cu_hpc
#SBATCH --partition=cpu
#SBATCH --job-name=example1
#SBATCH --output=example1.txt
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --time=00:10:00
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=1G

module purge

#To get worker node information
hostname
uname -a
more /proc/cpuinfo | grep "model name" | head -1
more /proc/cpuinfo | grep "processor" | wc -l

#To set your submission directory
echo "pwd = "`pwd`
export MYCODEDIR=`pwd`

#Check PATHs
echo "MYCODEDIR = "$MYCODEDIR
echo "TMPDIR = "$TMPDIR
echo "SLURM_SUBMIT_DIR = "$SLURM_SUBMIT_DIR
echo "SLURM_JOBID = "$SLURM_JOBID

#Move to TMPDIR and run python script
cp example1.py $TMPDIR
cd $TMPDIR
python example1.py >| test.log
ls -l
cp -rf test.log $MYCODEDIR/
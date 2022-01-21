# Slurm Job Submission

see also [e-Science official docs](https://phat-srimanobhas.gitbook.io/cu-e-science/)

QoS & Partition: https://phat-srimanobhas.gitbook.io/cu-e-science/slurm/slurm-qos-and-partition

Server Specification: https://phat-srimanobhas.gitbook.io/cu-e-science/introduction-to-our-cluster/our-resources

## Useful commands

```
> sinfo
```
![Alt text](/misc/images/sinfo.png "sinfo")
```
> squeue -u $(whoami)
```
![Alt text](/misc/images/watch_squeue.gif "watch squeue")

```
> scontrol show job 115927
```
![Alt text](/misc/images/115927.jpg "115927")

```
> scancel 115927
```

## Example sbatch script for GPU Task

```bash
#!/bin/bash
#SBATCH --partition=cpugpu
#SBATCH --qos=cu_hpc
#SBATCH --gpus=1
#SBATCH --cpus-per-task=2
#SBATCH --mem=8G

source ~/.bashrc
conda activate optml
ml purge
ml load GCC/8.3.0 CUDA/11.4.1 cuDNN/8.2.2.26-CUDA-11.4.1
python main.py
```

#!/bin/bash
#SBATCH --job-name=info
#SBATCH --output=%x-%j.out.log
#SBATCH --error=%x-%j.err.log
#SBATCH --partition=ndv4
#SBATCH --nodes=1
#SBATCH --ntasks=4
#SBATCH --cpus-per-task=1
#SBATCH --gpus=1

#### Print host & SLURM environment details ####
echo "===== Job allocation info ====="
echo "Job ID:          ${SLURM_JOB_ID:-<none>}"
echo "Job name:        ${SLURM_JOB_NAME:-<none>}"
echo "Partition:       ${SLURM_JOB_PARTITION:-<none>}"
echo "Nodes:           ${SLURM_JOB_NUM_NODES:-<none>}"
echo "Tasks:           ${SLURM_NTASKS:-<none>}"
echo "CPUs/task:       ${SLURM_CPUS_PER_TASK:-<none>}"
echo "Nodelist:        ${SLURM_JOB_NODELIST:-<none>}"
echo "Submit dir:      ${SLURM_SUBMIT_DIR:-$(pwd)}"
echo "Current host:    $(hostname)"
echo "Script directory:${SCRIPT_DIR}"
echo

#### System & hardware info ####
echo "===== CPU topology & memory ====="
lscpu
echo "----- Free memory -----"
free -h
echo

echo "===== GPU info (nvidia-smi) ====="
if command -v nvidia-smi &> /dev/null; then
    nvidia-smi --query-gpu=index,name,driver_version,memory.total,memory.used,utilization.gpu --format=csv
else
    echo "nvidia-smi not found in PATH"
fi
echo



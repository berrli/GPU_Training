#!/bin/bash
#SBATCH --job-name=test
#SBATCH --output=%x-%j.out.log
#SBATCH --error=%x-%j.err.log
#SBATCH --partition=ncv5
#SBATCH --nodes=1
#SBATCH --ntasks=16
#SBATCH --cpus-per-task=1
#SBATCH --gpus=1


#### Spack setup & activate “gpu_course” ####
echo "===== Spack setup ====="
# adjust to wherever you actually have Spack installed
SPACK_ROOT="${SPACK_ROOT:-$HOME/spack}"
if [[ -f "${SPACK_ROOT}/share/spack/setup-env.sh" ]]; then
    source "${SPACK_ROOT}/share/spack/setup-env.sh"
    spack env activate gpu_course
    echo "Active Spack env: $(spack env status)"
else
    echo "ERROR: could not find Spack at ${SPACK_ROOT}/share/spack/setup-env.sh"
fi
echo

#### Poetry setup & run cuda_check ####
echo "===== Poetry setup ====="
# Make sure your user‐install bin (where poetry lives) is on PATH
export PATH="$HOME/.local/bin:$PATH"

# sanity check
echo "Using poetry from: $(command -v poetry || echo '<not found>')"

if ! command -v poetry &> /dev/null; then
    echo "ERROR: poetry not found in ~/.local/bin; please verify installation"
    exit 1
fi

# enter your project and install deps
poetry install --no-interaction --no-ansi
echo "Poetry venv: $(poetry env info --path)"

# run your CUDA check
echo "===== Running CUDA check ====="
poetry run cuda_check
echo "cuda_check exit code: $?"
echo

echo "===== GPU info (nvidia-smi) ====="
if command -v nvidia-smi &> /dev/null; then
    nvidia-smi --query-gpu=index,name,driver_version,memory.total,memory.used,utilization.gpu --format=csv
else
    echo "nvidia-smi not found in PATH"
fi
echo

# Run the game of life 
echo "===== Running Game of Life Experiment ====="
pwd
# if nsys is already on your PATH (e.g. /usr/local/cuda/bin in your PATH)
nsys profile --sample=none --trace=cuda,nvtx -o ../output/${SLURM_JOB_NAME}_${SLURM_JOB_ID}_exp_report -- poetry run game_of_life_experiment_profiled --profile-gpu --profile-cpu




echo






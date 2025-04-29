import subprocess
import time
import matplotlib.pyplot as plt
import numpy as np
import os

# Ensure output directory exists
os.makedirs("../_static", exist_ok=True)

methods = {
    "NumPy (CPU)": "game_of_life_cpu",
    "CuPy (GPU)": "game_of_life_gpu",
    "Naive (CPU)": "game_of_life_naive",
}

grid_sizes = [50, 100, 250, 500, 1000, 2500, 5000, 10000]
timesteps_list = [100]  # multiple fixed timestep values
repeats = 3

# Loop over each timestep config to create a separate plot
for timesteps in timesteps_list:
    timing_results = {method: [] for method in methods}
    std_dev_results = {method: [] for method in methods}

    print(f"\n==== Running for {timesteps} timesteps ====")

    for size in grid_sizes:
        for method_name, entry_point in methods.items():
            run_times = []
            for repeat in range(repeats):
                cmd = [
                    "poetry", "run", entry_point,
                    "--size", str(size),
                    "--timesteps", str(timesteps)
                ]


                print(f"Running {method_name} | Grid: {size}x{size} | Timesteps: {timesteps} (Run {repeat+1}/{repeats})")

                start_time = time.perf_counter()
                subprocess.run(cmd)
                end_time = time.perf_counter()

                elapsed_time = end_time - start_time
                run_times.append(elapsed_time)

            timing_results[method_name].append(np.mean(run_times))
            std_dev_results[method_name].append(np.std(run_times))

    # Plotting
    plt.figure(figsize=(10, 6))

    for method_name in methods.keys():
        means = timing_results[method_name]
        stds = std_dev_results[method_name]
        plt.errorbar(grid_sizes, means, yerr=stds, label=method_name, marker='o', capsize=5)

    plt.title(f"Game of Life - Time vs Grid Size (Timesteps = {timesteps})")
    plt.xlabel("Grid Size (N x N)")
    plt.ylabel("Execution Time (seconds)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    filename = f"../_static/gol_time_vs_grid_timesteps_{timesteps}.png"
    plt.savefig(filename, dpi=300)
    print(f"Saved plot: {filename}")
    plt.close()

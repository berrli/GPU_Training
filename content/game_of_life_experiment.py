import subprocess
import time
import numpy as np
import os
import csv
import matplotlib.pyplot as plt

# Ensure output directory exists
os.makedirs("../_static", exist_ok=True)

def get_gpu_name():
    try:
        out = subprocess.check_output(
            ["nvidia-smi", "--query-gpu=name", "--format=csv,noheader"],
            stderr=subprocess.DEVNULL
        ).decode().strip().splitlines()
        return out[0]
    except Exception:
        return "Unknown_GPU"

def get_cpu_name():
    try:
        out = subprocess.check_output(["lscpu"], stderr=subprocess.DEVNULL).decode().splitlines()
        for line in out:
            if line.startswith("Model name:"):
                return line.split(":", 1)[1].strip()
    except Exception:
        pass
    return "Unknown_CPU"

def plot_timings(csv_filename):
    """
    Reads the CSV at csv_filename and reconstructs the error-bar plot:
    - x axis: grid_size
    - y axis: mean_time_sec, with yerr=std_dev_sec
    Saves a PNG with the same base name as the CSV.
    """
    # Read data back in
    data = {}
    timesteps = None
    with open(csv_filename, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            method = row["method"]
            size = int(row["grid_size"])
            mean_t = float(row["mean_time_sec"])
            std_t = float(row["std_dev_sec"])
            timesteps = row["timesteps"]  # same for every row
            if method not in data:
                data[method] = {"sizes": [], "means": [], "stds": []}
            data[method]["sizes"].append(size)
            data[method]["means"].append(mean_t)
            data[method]["stds"].append(std_t)

    # Make the plot
    plt.figure(figsize=(10, 6))
    for method, vals in data.items():
        plt.errorbar(
            vals["sizes"],
            vals["means"],
            yerr=vals["stds"],
            label=method,
            marker="o",
            capsize=5
        )
    plt.title(f"Game of Life - Time vs Grid Size (Timesteps = {timesteps})")
    plt.xlabel("Grid Size (N x N)")
    plt.ylabel("Execution Time (seconds)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    # Save the figure next to the CSV, with .png extension
    base = os.path.splitext(os.path.basename(csv_filename))[0]
    out_png = os.path.join(os.path.dirname(csv_filename), f"{base}.png")
    plt.savefig(out_png, dpi=300)
    plt.close()
    print(f"Saved plot: {out_png}")


# ——— Main benchmarking loop ———

gpu_name = get_gpu_name().replace(" ", "_")
cpu_name = get_cpu_name().replace(" ", "_")

methods = {
    "NumPy (CPU)": "game_of_life_cpu",
    "CuPy (GPU)": "game_of_life_gpu",
    "Naive (CPU)": "game_of_life_naive",
}

grid_sizes = [50, 100]
timesteps_list = [100]   # you can expand this list
repeats = 3

for timesteps in timesteps_list:
    csv_filename = f"../_static/gol_timings_{gpu_name}_{cpu_name}_ts{timesteps}.csv"
    with open(csv_filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "gpu", "cpu", "method",
            "grid_size", "timesteps",
            "mean_time_sec", "std_dev_sec"
        ])

        print(f"\n==== Running benchmarks for {timesteps} timesteps ====")
        for size in grid_sizes:
            for method_name, entry_point in methods.items():
                run_times = []
                for i in range(repeats):
                    cmd = [
                        "poetry", "run", entry_point,
                        "--size", str(size),
                        "--timesteps", str(timesteps)
                    ]
                    print(f"  {method_name:<12} | {size:6}×{size:<6} | run {i+1}/{repeats}")
                    t0 = time.perf_counter()
                    subprocess.run(cmd, check=True)
                    t1 = time.perf_counter()
                    run_times.append(t1 - t0)

                mean_t = np.mean(run_times)
                std_t = np.std(run_times)
                writer.writerow([
                    gpu_name, cpu_name,
                    method_name,
                    size, timesteps,
                    f"{mean_t:.6f}",
                    f"{std_t:.6f}"
                ])

    print(f"Saved CSV: {csv_filename}")

    # Now generate the plot from that CSV
    plot_timings(csv_filename)

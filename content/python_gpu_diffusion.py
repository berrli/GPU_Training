import xarray as xr
import plotly.graph_objects as go
import argparse
import cupy
from pathlib import Path
import sys
import platform
import cupy._core

# Define the root directory
ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"
OUTPUT_DIR = ROOT_DIR / "output"
DATA_FILE = "cmems_mod_glo_phy-thetao_anfc_0.083deg_PT6H-i_thetao_13.83W-6.17E_46.83N-65.25N_0.49-5727.92m_2024-01-01-2024-01-07.nc"



def load_temperature_data(num_depths, num_time_steps):
    # Load the NetCDF file
    data = xr.open_dataset(DATA_FILE)
    temperature = data['temperature']  # Replace 'temperature' with the actual variable name

    # Prepare data for the specified number of depth and time levels
    depths = temperature['depth'].values[:num_depths]
    time_steps = temperature['time'].values[:num_time_steps]
    latitudes = temperature['latitude'].values
    longitudes = temperature['longitude'].values

    # Extract temperature values
    temperature_values = temperature.isel(
        depth=slice(0, num_depths), time=slice(0, num_time_steps)
    ).values

    return latitudes, longitudes, depths, time_steps, temperature_values

def diffuse_temperature(temperature, dt, dx, dy, dz, D, num_steps):
    # Convert temperature data to GPU using CuPy
    temperature_gpu = cp.asarray(temperature)
    
    def diffusion_step(temp):
        # Apply the diffusion formula in 3D
        laplacian = (
            (cp.roll(temp, 1, axis=0) - 2 * temp + cp.roll(temp, -1, axis=0)) / dx**2 +
            (cp.roll(temp, 1, axis=1) - 2 * temp + cp.roll(temp, -1, axis=1)) / dy**2 +
            (cp.roll(temp, 1, axis=2) - 2 * temp + cp.roll(temp, -1, axis=2)) / dz**2
        )
        return temp + D * laplacian * dt
    
    # Run diffusion for the specified number of steps
    for step in range(num_steps):
        temperature_gpu = diffusion_step(temperature_gpu)
    
    return cp.asnumpy(temperature_gpu)  # Move to CPU for final calculations

def compute_statistics(initial_temperature, final_temperature):
    # Compute initial statistics
    initial_mean = cp.mean(initial_temperature)
    initial_max = cp.max(initial_temperature)
    initial_min = cp.min(initial_temperature)

    # Compute final statistics
    final_mean = cp.mean(final_temperature)
    final_max = cp.max(final_temperature)
    final_min = cp.min(final_temperature)

    # Compute differences
    mean_change = final_mean - initial_mean
    max_change = final_max - initial_max
    min_change = final_min - initial_min

    # Print statistics
    print("Initial Temperature Statistics:")
    print(f"Mean Temperature: {initial_mean:.2f} °C")
    print(f"Max Temperature: {initial_max:.2f} °C")
    print(f"Min Temperature: {initial_min:.2f} °C\n")

    print("Final Temperature Statistics:")
    print(f"Mean Temperature: {final_mean:.2f} °C")
    print(f"Max Temperature: {final_max:.2f} °C")
    print(f"Min Temperature: {final_min:.2f} °C\n")

    print("Change in Temperature Statistics:")
    print(f"Mean Temperature Change: {mean_change:.2f} °C")
    print(f"Max Temperature Change: {max_change:.2f} °C")
    print(f"Min Temperature Change: {min_change:.2f} °C")

def run_benchmark():
    parser = argparse.ArgumentParser(description="Process 3D temperature dispersion and show statistics.")
    parser.add_argument("--num_depths", type=int, default=5, help="Number of depth levels.")
    parser.add_argument("--num_time_steps", type=int, default=10, help="Number of time steps.")

    args = parser.parse_args()

    # Load initial temperature data
    latitudes, longitudes, depths, time_steps, initial_temperature = load_temperature_data(
        num_depths=args.num_depths,
        num_time_steps=args.num_time_steps
    )

    # Run the diffusion process
    final_temperature = diffuse_temperature(
        initial_temperature, dt=0.1, dx=1, dy=1, dz=1, D=0.01, num_steps=args.num_time_steps
    )

    # Compute and print statistics
    compute_statistics(initial_temperature, final_temperature)
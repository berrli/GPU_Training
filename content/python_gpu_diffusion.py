import xarray as xr
from pathlib import Path
import argparse
import time
import xarray as xr
import numpy as np
import cupy as cp
from tqdm import tqdm 

# Define the root directory
ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"
OUTPUT_DIR = ROOT_DIR / "output"
DATA_FILE = "cmems_mod_glo_phy-thetao_anfc_0.083deg_PT6H-i_thetao_13.83W-6.17E_46.83N-65.25N_0.49-5727.92m_2024-01-01-2024-01-02.nc"
OUTPUT_FILE_NUMPY = "predicted_temperatures_numpy.nc"
OUTPUT_FILE_CUPY = "predicted_temperatures_cupy.nc"


# Load the NetCDF data
def load_data():
    file_path = DATA_DIR / DATA_FILE
    return xr.open_dataset(file_path)


def save_to_netcdf(data, new_temperature, output_file_path, num_timesteps):
    # Adjust new_temperature to have only num_timesteps or fewer
    new_temperature = new_temperature[:num_timesteps]  # Only include the desired number of timesteps

    # Generate a new time coordinate as a sequence of numbers (1, 2, ..., num_timesteps)
    time_coord = range(1, num_timesteps + 1)

    # Create a new dataset with original depth, latitude, and longitude coordinates
    output_data = xr.Dataset(
        {'thetao': (('time', 'depth', 'latitude', 'longitude'), new_temperature)},
        coords={
            'time': time_coord,  # Sequential time coordinate
            'depth': data['depth'].values,  # Use original depth coordinates
            'latitude': data['latitude'].values,  # Use original latitude coordinates
            'longitude': data['longitude'].values  # Use original longitude coordinates
        },
    )
    output_data.to_netcdf(output_file_path, engine='netcdf4')



import numpy as np
import time
from tqdm import tqdm

# Temperature diffusion function using NumPy with masking for boundaries
def temperature_diffusion_numpy(data, num_timesteps, diffusion_coeff=0.1):
    temperature = np.asarray(data['thetao'].values)  # Convert to a NumPy array
    temperature = temperature[0:1, :, :, :]
    temperature = np.tile(temperature, (num_timesteps, 1, 1, 1))
    
    # Summary statistics
    summary = {
        "mean": np.mean(temperature),
        "min": np.min(temperature),
        "max": np.max(temperature),
        "median": np.median(temperature),
    }
    print(summary)
    
    mask = ~np.isnan(temperature)  # Mask: True for ocean points, False for NaN regions (land)
    new_temperature = np.copy(temperature)
    timestep_durations = []

    # Extract the first timestamp and create a new time coordinate for the predicted timesteps
    original_time = data['time'].values
    time_coord = np.array([original_time[0] + np.timedelta64(i, 'D') for i in range(num_timesteps)])

    # Run the diffusion model
    for t in tqdm(range(num_timesteps), desc="NumPy Diffusion Progress"):
        start_time = time.time()

        # Apply diffusion calculation with mask-based boundary handling
        temp_copy = temperature[1:-1, 1:-1, 1:-1]  # Core section without boundaries
        neighbor_sum = np.zeros_like(temp_copy)
        neighbor_count = np.zeros_like(temp_copy)

        # Sum available neighbors and count them only for valid ocean points
        if mask[:-2, 1:-1, 1:-1].any():  # Front
            neighbor_sum += np.where(mask[:-2, 1:-1, 1:-1], temperature[:-2, 1:-1, 1:-1], 0)
            neighbor_count += mask[:-2, 1:-1, 1:-1]

        if mask[2:, 1:-1, 1:-1].any():  # Back
            neighbor_sum += np.where(mask[2:, 1:-1, 1:-1], temperature[2:, 1:-1, 1:-1], 0)
            neighbor_count += mask[2:, 1:-1, 1:-1]

        if mask[1:-1, :-2, 1:-1].any():  # Left
            neighbor_sum += np.where(mask[1:-1, :-2, 1:-1], temperature[1:-1, :-2, 1:-1], 0)
            neighbor_count += mask[1:-1, :-2, 1:-1]

        if mask[1:-1, 2:, 1:-1].any():  # Right
            neighbor_sum += np.where(mask[1:-1, 2:, 1:-1], temperature[1:-1, 2:, 1:-1], 0)
            neighbor_count += mask[1:-1, 2:, 1:-1]

        if mask[1:-1, 1:-1, :-2].any():  # Bottom
            neighbor_sum += np.where(mask[1:-1, 1:-1, :-2], temperature[1:-1, 1:-1, :-2], 0)
            neighbor_count += mask[1:-1, 1:-1, :-2]

        if mask[1:-1, 1:-1, 2:].any():  # Top
            neighbor_sum += np.where(mask[1:-1, 1:-1, 2:], temperature[1:-1, 1:-1, 2:], 0)
            neighbor_count += mask[1:-1, 1:-1, 2:]

        # Apply diffusion to valid points only, avoiding NaN regions
        new_temperature[1:-1, 1:-1, 1:-1] = np.where(
            mask[1:-1, 1:-1, 1:-1],
            temp_copy + diffusion_coeff * (neighbor_sum - 6 * temp_copy) / np.maximum(neighbor_count, 1),
            temperature[1:-1, 1:-1, 1:-1]
        )

        timestep_durations.append(time.time() - start_time)
        temperature = new_temperature
        
    # Convert to final temperature and save
    final_temperature = new_temperature

    print("The size of the final temperature is: " + str(final_temperature.shape))
    
    # Save to NetCDF (assuming you have a `save_to_netcdf` function defined)
    save_to_netcdf(data, final_temperature, DATA_DIR / OUTPUT_FILE_NUMPY, num_timesteps)

    avg_time_per_timestep = sum(timestep_durations) / num_timesteps
    print(f"NumPy model completed in {sum(timestep_durations):.4f} seconds. "
          f"Average time per timestep: {avg_time_per_timestep:.4f} seconds.")


    
def run_diffusion_numpy():
    parser = argparse.ArgumentParser(description="Run 3D Diffusion Model with Numpy")
    parser.add_argument("--num_timesteps", type=int, default=300, help="Number of Timesteps to run for")

    args = parser.parse_args()

    # Pass parsed arguments to visualisation_slice
    temperature_diffusion_numpy(data=load_data(), num_timesteps=args.num_timesteps)

# # Temperature diffusion function using CuPy with masking for boundaries
def temperature_diffusion_cupy(data, num_timesteps, diffusion_coeff=0.5):
    temperature = cp.asarray(data['thetao'].values)  # Convert to a CuPy array
    temperature = temperature[0:1, :, :, :]
    temperature = np.tile(temperature, (num_timesteps, 1, 1, 1))
    # Summary statistics
    summary = {
        "mean": np.mean(temperature),
        "min": np.min(temperature),
        "max": np.max(temperature),
        "median": np.median(temperature),
    }

    print(summary)
    mask = ~cp.isnan(temperature)  # Mask: True for ocean points, False for NaN regions (land)
    new_temperature = cp.copy(temperature)
    timestep_durations = []

    # Extract the first timestamp and create a new time coordinate for the predicted timesteps
    original_time = data['time'].values
    time_coord = np.array([original_time[0] + np.timedelta64(i, 'D') for i in range(num_timesteps)])

    # Run the diffusion model
    for t in tqdm(range(num_timesteps), desc="CuPy Diffusion Progress"):
        start_time = time.time()

        # Apply diffusion calculation with mask-based boundary handling
        temp_copy = temperature[1:-1, 1:-1, 1:-1]  # Core section without boundaries
        neighbor_sum = cp.zeros_like(temp_copy)
        neighbor_count = cp.zeros_like(temp_copy)

        # Sum available neighbors and count them only for valid ocean points
        if mask[:-2, 1:-1, 1:-1].any():  # Front
            neighbor_sum += cp.where(mask[:-2, 1:-1, 1:-1], temperature[:-2, 1:-1, 1:-1], 0)
            neighbor_count += mask[:-2, 1:-1, 1:-1]

        if mask[2:, 1:-1, 1:-1].any():  # Back
            neighbor_sum += cp.where(mask[2:, 1:-1, 1:-1], temperature[2:, 1:-1, 1:-1], 0)
            neighbor_count += mask[2:, 1:-1, 1:-1]

        if mask[1:-1, :-2, 1:-1].any():  # Left
            neighbor_sum += cp.where(mask[1:-1, :-2, 1:-1], temperature[1:-1, :-2, 1:-1], 0)
            neighbor_count += mask[1:-1, :-2, 1:-1]

        if mask[1:-1, 2:, 1:-1].any():  # Right
            neighbor_sum += cp.where(mask[1:-1, 2:, 1:-1], temperature[1:-1, 2:, 1:-1], 0)
            neighbor_count += mask[1:-1, 2:, 1:-1]

        if mask[1:-1, 1:-1, :-2].any():  # Bottom
            neighbor_sum += cp.where(mask[1:-1, 1:-1, :-2], temperature[1:-1, 1:-1, :-2], 0)
            neighbor_count += mask[1:-1, 1:-1, :-2]

        if mask[1:-1, 1:-1, 2:].any():  # Top
            neighbor_sum += cp.where(mask[1:-1, 1:-1, 2:], temperature[1:-1, 1:-1, 2:], 0)
            neighbor_count += mask[1:-1, 1:-1, 2:]

        # Apply diffusion to valid points only, avoiding NaN regions
        new_temperature[1:-1, 1:-1, 1:-1] = cp.where(
            mask[1:-1, 1:-1, 1:-1],
            temp_copy + diffusion_coeff * (neighbor_sum - 6 * temp_copy) / cp.maximum(neighbor_count, 1),
            temperature[1:-1, 1:-1, 1:-1]
        )

        cp.cuda.Stream.null.synchronize()  # Wait for the GPU computation to complete
        timestep_durations.append(time.time() - start_time)
        temperature = new_temperature

        

        # summary = {
        # "mean": np.nanmean(temperature),
        # "min": np.nanmin(temperature),
        # "max": np.nanmax(temperature),
        # "median": np.nanmedian(temperature),
        # }
        # print(summary)
    # Convert back to NumPy and save
    final_temperature = cp.asnumpy(new_temperature)

    print("The size of the final temperature is: " + str(final_temperature.shape))

    save_to_netcdf(data, final_temperature, DATA_DIR / OUTPUT_FILE_CUPY, num_timesteps)

    avg_time_per_timestep = sum(timestep_durations) / num_timesteps
    print(f"CuPy model completed in {sum(timestep_durations):.4f} seconds. "
          f"Average time per timestep: {avg_time_per_timestep:.4f} seconds.")




    
def run_diffusion_cupy():
    parser = argparse.ArgumentParser(description="Run 3D Diffusion Model with CuPy")
    parser.add_argument("--num_timesteps", type=int, default=300, help="Number of Timesteps to run for")

    args = parser.parse_args()

    # Pass parsed arguments to visualisation_slice
    temperature_diffusion_cupy(data=load_data(), num_timesteps=args.num_timesteps)

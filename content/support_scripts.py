import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from pathlib import Path
import plotly.graph_objects as go
import argparse
import subprocess
import os

# Define the root directory
ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"
OUTPUT_DIR = ROOT_DIR / "output"
DATA_FILE = "cmems_mod_glo_phy-thetao_anfc_0.083deg_PT6H-i_thetao_13.83W-6.17E_46.83N-65.25N_0.49-5727.92m_2024-01-01-2024-01-07.nc"

def download_ocean_data():
    # Define the command as a list
    command = [
        "poetry", "run", "copernicusmarine", "subset",
        "--dataset-id", "cmems_mod_glo_phy-thetao_anfc_0.083deg_PT6H-i",
        "--variable", "thetao",
        "--start-datetime", "2024-01-01T00:00:00",
        "--end-datetime", "2024-01-07T00:00:00",
        "--minimum-longitude", "-13.903248235212025",
        "--maximum-longitude", "6.186015157645116",
        "--minimum-latitude", "46.82995633719309",
        "--maximum-latitude", "65.31207865862164",
        "--minimum-depth", "0.49402499198913574",
        "--maximum-depth", "5727.9169921875"
    ]

    os.chdir(DATA_DIR)
    
    try:
        # Run the command and enable interactive mode by attaching directly to the terminal's stdin/stdout
        result = subprocess.run(command, check=True)
        print("Data downloaded successfully.")
    except subprocess.CalledProcessError as e:
        print("An error occurred:", e)
    finally:
        # Change back to the original directory
        os.chdir(DATA_DIR)

def summary():
    # Load the NetCDF file from the data directory
    file_path = DATA_DIR / DATA_FILE
    data = xr.open_dataset(file_path)

    # Assume the variable of interest is named 'temperature' (check the variable name in your file)
    temperature = data['thetao']

    # Print some summary statistics
    print("Temperature Summary Statistics:")
    print("Mean temperature:", temperature.mean().item())
    print("Max temperature:", temperature.max().item())
    print("Min temperature:", temperature.min().item())
    print("Standard deviation:", temperature.std().item())

    # Optional: Print information about dimensions and coordinates
    print("\nDataset Dimensions and Coordinates:")
    print(data)


def visualisation_static():
    # Load the NetCDF file
    file_path = DATA_DIR / DATA_FILE
    data = xr.open_dataset(file_path)

    # Assume the variable of interest is named 'temperature' (check the variable name in your file)
    temperature = data['thetao']

    # Select a subset for plotting (e.g., take a single depth level or time step)
    # Adjust these selections based on your dataset's structure
    temperature_subset = temperature.isel(time=0, depth=0)  # First time step and surface level

    # Prepare data for 2D plotting
    latitudes = temperature_subset['latitude'].values
    longitudes = temperature_subset['longitude'].values
    temperature_values = temperature_subset.values

    # Create a 2D plot of the temperature data
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot the temperature data as a heatmap
    c = ax.pcolormesh(longitudes, latitudes, temperature_values, shading='auto', cmap='viridis')
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    ax.set_title('Ocean Surface Temperature')

    # Add a color bar for the temperature values
    fig.colorbar(c, ax=ax, label='Temperature (°C)')

    # Save the figure to disk in the output directory
    save_path = OUTPUT_DIR / "temperature_slice.png"
    plt.savefig(save_path, format='png', dpi=300, bbox_inches='tight')

    # Optionally, close the figure after saving to free memory
    plt.close(fig)




def visualisation_slice():
    # Load the NetCDF file
    file_path = DATA_DIR / DATA_FILE
    data = xr.open_dataset(file_path)

    # Assume the variable of interest is named 'temperature' (check the variable name in your file)
    temperature = data['thetao']

    # Select a subset for plotting (e.g., take a single depth level or time step)
    temperature_subset = temperature.isel(time=0, depth=0)  # First time step and surface level

    # Prepare data for 2D plotting
    latitudes = temperature_subset['latitude'].values
    longitudes = temperature_subset['longitude'].values
    temperature_values = temperature_subset.values

    # Create the interactive heatmap
    fig = go.Figure(data=go.Heatmap(
        z=temperature_values,
        x=longitudes,
        y=latitudes,
        colorscale='Viridis',
        colorbar=dict(title='Temperature (°C)')
    ))

    # Set labels and title
    fig.update_layout(
        title="Ocean Surface Temperature",
        xaxis_title="Longitude",
        yaxis_title="Latitude"
    )

    # Save the interactive plot as an HTML file
    save_path = OUTPUT_DIR / "temperature_slice_interactive.html"
    fig.write_html(save_path)

def plot_cube(num_depths=3, num_time_steps=3):
    # Load the NetCDF file
    file_path = DATA_DIR / DATA_FILE
    data = xr.open_dataset(file_path)

    # Assume the variable of interest is named 'temperature' (check the variable name in your file)
    temperature = data['thetao']

    # Prepare data for 3D plotting (take the specified number of depth and time levels)
    latitudes = temperature['latitude'].values
    longitudes = temperature['longitude'].values
    depths = temperature['depth'].values[:num_depths]
    time_steps = temperature['time'].values[:num_time_steps]
    temperature_values = temperature.isel(depth=slice(0, num_depths), time=slice(0, num_time_steps)).values

    # Create the figure and define frames for each time step
    fig = go.Figure()

    # Create initial frame (first time step)
    for i, depth in enumerate(depths):
        fig.add_trace(go.Surface(
            z=[[depth] * len(longitudes) for _ in range(len(latitudes))],
            x=longitudes,
            y=latitudes,
            surfacecolor=temperature_values[0, i],
            colorscale='Viridis',
            colorbar=dict(title='Temperature (°C)')
        ))

    # Define frames for each subsequent time step
    frames = []
    for t, time in enumerate(time_steps):
        frame_data = []
        for i, depth in enumerate(depths):
            frame_data.append(go.Surface(
                z=[[depth] * len(longitudes) for _ in range(len(latitudes))],
                x=longitudes,
                y=latitudes,
                surfacecolor=temperature_values[t, i],
                colorscale='Viridis'
            ))
        frames.append(go.Frame(data=frame_data, name=f"Time {t}"))

    fig.frames = frames

    # Set up play button and slider
    fig.update_layout(
        title="3D Ocean Temperature Profile Over Time",
        scene=dict(
            xaxis_title="Longitude",
            yaxis_title="Latitude",
            zaxis_title="Depth (m)",
            zaxis=dict(autorange="reversed")
        ),
        updatemenus=[{
            "type": "buttons",
            "showactive": False,
            "buttons": [{
                "label": "Play",
                "method": "animate",
                "args": [None, {"frame": {"duration": 500, "redraw": True}, "fromcurrent": True}]
            }, {
                "label": "Pause",
                "method": "animate",
                "args": [[None], {"frame": {"duration": 0, "redraw": False}, "mode": "immediate", "transition": {"duration": 0}}]
            }]
        }],
        sliders=[{
            "active": 0,
            "yanchor": "top",
            "xanchor": "left",
            "currentvalue": {
                "font": {"size": 20},
                "prefix": "Time Step: ",
                "visible": True,
                "xanchor": "right"
            },
            "steps": [{
                "label": f"{t}",
                "method": "animate",
                "args": [[f"Time {t}"], {"frame": {"duration": 500, "redraw": True}, "mode": "immediate", "transition": {"duration": 0}}]
            } for t in range(len(time_steps))]
        }]
    )

    # Save the interactive plot as an HTML file
    save_path = OUTPUT_DIR / "temperature_3d_profile_interactive.html"
    fig.write_html(save_path)

def visualisation_cube():
    parser = argparse.ArgumentParser(description="Visualize a 3D temperature cube.")
    parser.add_argument("--num_depths", type=int, default=5, help="Number of depth levels.")
    parser.add_argument("--num_time_steps", type=int, default=3, help="Number of time steps.")

    args = parser.parse_args()

    # Pass parsed arguments to visualisation_cube
    plot_cube(num_depths=args.num_depths, num_time_steps=args.num_time_steps)



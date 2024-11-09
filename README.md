# GPU Training Course 

This repository contains all of the materials for the running of a GPU Training Course.

# Installation Instructions 

The following provides the steps that are required to install the necessary compilers and packages to engage with the material in this course.

## Spack - Installing system-level requirements
Within this course [Spack](https://spack.io/) is being used to manage the system-level requirements, such as drivers. The reason for this is that alot of system-level requirements generally require priveleged permissions, such as the access to use of `sudo`. However as alot of the platforms that have GPUs available are HPC platforms, spack allows us to install drivers that normally would require privleged access without. There are also a range of other benefits to the use of spack that will be discussed in this course. 

First you will need to clone the spack repo:
``` bash
git clone https://github.com/spack/spack.git
```

You will then need to activate spack with:
```bash 
source spack/share/spack/setup-env.sh
```
> [!NOTE]
> You can check that spack has been successfully installed by running `spack --version` which should return the version of spack that you have available. 

You will need need to create a spack environment, which can be done with the following, creating a spack environment named "cuda_course"
```bash 
spack env create cuda_course
```
which can then be activated with
```bash 
spack env activate -p cuda_course
```

In this course, spack is being used to install system level requirements, and so the required version of python and the needed driver of CUDA are installed via spack, with the following two commands. 
```bash
spack add python@3.12 
spack add cuda
```
> [!NOTE]
> This step will simply say that you intend to install these packages, at this time spack is still waiting for more packages to be added to the environment specification. We can check what the current specification is (e.g. package list, dependecies, compilers to be used etc.) with `spack spec`.

Finally we are able to install all of the pakcages into out spack environment with 
```bash 
spack install
```

## Poetry - Installing user-level requirements

Within this course, [Poetry](https://python-poetry.org/) is used to manage the user-level requirements. 

Poetry can be installed by the following command: 
```bash 
curl -sSL https://install.python-poetry.org | python3 -
```
> [!NOTE]
> Poetry can be uninstalled with `curl -sSL https://install.python-poetry.org | python3 - --uninstall`.

All of the user-level requirements can be installed via Poetry with the command:
```bash
poetry install
```
> [!NOTE]
> `poetry install` needs to be ran from within the training course repo. If you havnt then you need to clone this repo with `git clone https://github.com/berrli/GPU_Training` and then navigate to its root with `cd GPU_Training`

> [!NOTE]
> You can check that the installation has been successful by running `poetry run cuda_check`, which should return the number of CUDA devices that are currently avaiable, such as `Number of CUDA devices: 1`. If you want to find out more information about the device that is connected you can run a command such as `nvidia-smi` for a NVIDIA GPU.

## Helpful Auxiliary Software

This section details a number of different useful pieces of software for making the development of GPU code easier. Notably alot of these sit within Visual Studio Code, chosen as these are what the author was exposed to when first starting out in GPU development. 

### Using Visual Studio Code (VSCode)

Visual Studio Code (VSCode) can be installed from its website [here](https://code.visualstudio.com/).

#### Remote-SSH

This guide walks you through setting up and using **Remote-SSH** in Visual Studio Code (VSCode) to connect to a remote machine.

##### Install the Remote - SSH Extension

1. Open **VSCode**.
2. Go to the **Extensions** view by clicking on the square icon in the sidebar or pressing `Ctrl+Shift+X` (Windows/Linux) or `Cmd+Shift+X` (Mac).
3. Search for "**Remote - SSH**" and install the extension from Microsoft.

##### Configure SSH on Your Local Machine

Ensure you can SSH into the remote machine from your terminal. If SSH is not already configured:

1. **Generate SSH Keys** (if not already done):
   - Open a terminal on your local machine.
   - Run the command `ssh-keygen` and follow the prompts to generate a key pair. This will create keys in `~/.ssh/` by default.
   
2. **Copy Your Public Key to the Remote Machine**:
   - Run the command `ssh-copy-id user@hostname`, replacing `user` and `hostname` with your remote machine’s username and IP address or hostname.
   - Enter your password when prompted. This step ensures you can log in without repeatedly typing your password.

##### Add SSH Configuration in VSCode

1. Open **VSCode**.
2. Press `Ctrl+Shift+P` (Windows/Linux) or `Cmd+Shift+P` (Mac) to open the command palette.
3. Type and select **Remote-SSH: Open Configuration File**.
4. Choose the SSH configuration file (usually located at `~/.ssh/config`).

5. Add a new SSH configuration to the file, specifying the remote machine’s details. Here’s an example configuration:

   ```plaintext
   Host my-remote-machine
       HostName <remote-ip-or-hostname>
       User <your-username>
       IdentityFile ~/.ssh/id_rsa  # Path to your SSH private key
       Port 22  # Default SSH port; change if needed

##### Connecting to remote from within VSCode

You should now be able to connect to the remote machine from within VSCode but using `Ctrl+Shift+P` (Windows/Linux) or `Cmd+Shift+P` (Mac) and then selecting `Remote-SSH: Connect to host...` which should then present a list with the name of the machien you gave in the config file, in the above case `my-remote-machine`. You will then be asked for a password if you protected your ssh key. Once connected a new VSCode window will be created and you should have a fully functioning ID on the remote machine.


#### Live Server 

As this course produces 3D outputs, some supporting code will generate interactive HTML dashboards to make exploring the output data easier. The VSCode Live Server extension makes the process of viewing these dashboards with your local web browser easier. 

##### Install the Live Server Extension

1. Open **VSCode**.
2. Go to the **Extensions** view by clicking on the square icon in the sidebar or pressing `Ctrl+Shift+X` (Windows/Linux) or `Cmd+Shift+X` (Mac).
3. Search for "**Live Server**" and install the extension by **Ritwick Dey**.

---

##### Start the Live Server

1. **Right-click** on the HTML file in the editor and select **Open with Live Server**.

##### View Changes in Real-Time

- As you edit and save your HTML, CSS, or JavaScript files, the browser will automatically refresh to display your changes.
- This eliminates the need to manually refresh the browser, speeding up development.

# Data
## Data Download

To download the dataset, follow these steps:

- **Create a Copernicus Marine Account**:
   - You will need an account to access the data. Register here: [Register for Account](https://data.marine.copernicus.eu/register?redirect=%2Fproduct%2FGLOBAL_ANALYSISFORECAST_PHY_001_024%2Fdownload%3Fdataset%3Dcmems_mod_glo_phy-thetao_anfc_0.083deg_PT6H-i_202406).

-  **Run the CLI Command to Download the Dataset**:
   - Use the following command to download the subset of data:
     ```bash
     poetry run download_data
     ```
   - This command will prompt you to enter your username and password. Once authenticated, the data file will download to the data directory. Please note that the download may take some time as the file size is approximately 250 MB.

## Data Description 

The dataset used during the course is based on 3-Dimensional Ocean Temperatures. The dataset is described in detail on the [Copernicus Marine Data Service](https://data.marine.copernicus.eu/product/GLOBAL_ANALYSISFORECAST_PHY_001_024/description)

**Filename**: `cmems_mod_glo_phy-thetao_anfc_0.083deg_PT6H-i_1730799065517.nc`

**Description**:  
This dataset was downloaded from the **Global Ocean Physics Analysis and Forecast** service. It provides data for global ocean physics, focusing on sea water potential temperature.

- **Product Identifier**: `GLOBAL_ANALYSISFORECAST_PHY_001_024`
- **Product Name**: Global Ocean Physics Analysis and Forecast
- **Dataset Identifier**: `cmems_mod_glo_phy-thetao_anfc_0.083deg_PT6H-i`

**Variable Visualized**:  
- **Sea Water Potential Temperature (thetao)**: Measured in degrees Celsius [°C].

**Geographical Area of Interest**:  
- **Region**: Around the United Kingdom
- **Coordinates**:
  - **Northern Latitude**: 65.312
  - **Eastern Longitude**: 6.1860
  - **Southern Latitude**: 46.829
  - **Western Longitude**: -13.90

**Depth Range**:  
- **Minimum Depth**: 0.49 meters  
- **Maximum Depth**: 5727.9 meters

**File Size**:  
- **267.5 MB**


Filename `cmems_mod_glo_phy-thetao_anfc_0.083deg_PT6H-i_1730799065517.nc`: A dataset downloaded from the Global Ocean Physics Analysis and Forecast service. Product Identifier Product identifier
GLOBAL_ANALYSISFORECAST_PHY_001_024, Product Name: Global Ocean Physics ANalysis and Forecast, with the dataset as: cmems_mod_glo_phy-thetao_anfc_0.083deg_PT6H-i. The variable visualised is Sea water potential temperature thetao [°C]. 
The area of interest that was selected was around the UK with the variables of N: 65.312, E:6.1860, S:46.829, W:-13.90. The depth that is being used is: 0.49m to 5727.9m. The file size for the file is 267.5MB.

# Tips and Tricks

Programming GPUs can be pretty complex, particularly during the set-up phase, where a number of different drivers are required to run code on the GPU. This section provides some potential lines of inquiry as to what may be causing issues with your current set-up if you are entirely stuck based on personal past experiences of common faults. 

## PATH
In UNIX, **PATH** is an environment variable listing directories to search for commands. If a command isn’t found, it’s likely the directory containing it isn’t in PATH. However, due to the number of different versions of software used in these projects, such as having the same package compiled with different compilers, e.g. GCC for OpenMP or NVHPC-related compilers for OpenACC, then a misconfigured PATH can be a common cause of issues. The use of `which <command>` will help you to identify what is being run when you use that line on the command line. You can see this clearly within this project, where there is a python used by spack and then also a python used by poetry, where they share the same version, but their distinguishing factor is where they are located in regards to the file path. 

## Starting Fresh 

Sometimes, with the number of different elements involved in a GPU project, it can be helpful to clean the workspace and start fresh. To remove spack, you will also need to remove the `.spack` directory alongside the `spack` directory. If you don't remove the hidden directory and then simply clone the spack repo again, then you may find that the issue with the spack might be persistent from elements left in the hidden directory. 

TODO:

The method that currently saves he simulation code there is a known issue wehre due to the original NetCDF being used you cant exceed the numer of timesteps that are being used. This is somethign that will need to be changed in the future. Hopefully this can be solved simply with the save_to_netcdf function that will copy the dimensions for the depth, lat and long since those will remain constant. 

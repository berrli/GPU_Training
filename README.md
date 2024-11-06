# GPU Training Course 

## Installation Instructions 

The following provides the steps that are required to install the necessary compilers and packages to engage with the material in this course.

### Spack - Installing system-level requirements
Within this course [Spack](https://spack.io/) is being used to manage the system-level requirements, such as drivers. The reason for this is that alot of system-level requirements generally require priveleged permissions, such as the access to use of `sudo`. However as alot of the platforms that have GPUs available are HPC platforms, spack allows us to install drivers that normally would require privleged access without. There are also a range of other benefits to the use of spack that will be discussed in this course. 

First you will need to clone the spack repo:
``` bash
git clone https://github.com/spack/spack.git
```

You will then need to activate spack with:
```bash 
source spack/share/spack/setup-env.sh
```
> [!CHECK]
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

### Poetry - Installing user-level requirements

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

> [!CHECK]
> You can check that the installation has been successful by running `poetry run cuda_check`, which should return the number of CUDA devices that are currently avaiable, such as `Number of CUDA devices: 1`. If you want to find out more information about the device that is connected you can run a command such as `nvidia-smi` for a NVIDIA GPU.

## Helpful Auxiliary Software

### Using VSCode 

#### Remote-SSH

#### Live Server 

## Adding Live Server extention 
You can open a HTML file with a right click and then select `Open With Live Server` that will let you open the HTML file with your browser. This makes having an interactive plot in the easiest way. 
## Connecting to the GPU platforms

Go through using VSCode and using the Remote-SSH to then get access to the platform.

## Running some example code
A repo for a range of materials that can be used to learn about GPU training and so important topics throughout. 

This course makes use of peotry through. You can install poetry with the following command: `curl -sSL https://install.python-poetry.org | python3 -`.

You can then use poetry to install the needed requirements with `poetry install`.

You can then activate the environment that has been created with `poetry shell`. 


Everything is intended to be ran from the root directory. TODO: Change it so that the file path are alot more robust and these can be ran from anywehre


# Data Description 

## 3D Global Ocean Temperatures 

Filename `cmems_mod_glo_phy-thetao_anfc_0.083deg_PT6H-i_1730799065517.nc`: A dataset downloaded from the Global Ocean Physics Analysis and Forecast service. Product Identifier Product identifier
GLOBAL_ANALYSISFORECAST_PHY_001_024, Product Name: Global Ocean Physics ANalysis and Forecast, with the dataset as: cmems_mod_glo_phy-thetao_anfc_0.083deg_PT6H-i. The variable visualised is Sea water potential temperature thetao [°C]. 
The area of interest that was selected was around the UK with the variables of N: 65.312, E:6.1860, S:46.829, W:-13.90. The depth that is being used is: 0.49m to 5727.9m. The file size for the file is 267.5MB. 


## Data download 

The only thing you need to do is to install the CLI with `pip install copernicusmarine`, described here: https://pypi.org/project/copernicusmarine/

You will also need to create an account here: [Register for Account](https://data.marine.copernicus.eu/register?redirect=%2Fproduct%2FGLOBAL_ANALYSISFORECAST_PHY_001_024%2Fdownload%3Fdataset%3Dcmems_mod_glo_phy-thetao_anfc_0.083deg_PT6H-i_202406)

You will then need to the data directory with `cd data`.

The CLI command for the data is: 

`copernicusmarine subset --dataset-id cmems_mod_glo_phy-thetao_anfc_0.083deg_PT6H-i --variable thetao --start-datetime 2024-01-01T00:00:00 --end-datetime 2024-01-07T00:00:00 --minimum-longitude -13.903248235212025 --maximum-longitude 6.186015157645116 --minimum-latitude 46.82995633719309 --maximum-latitude 65.31207865862164 --minimum-depth 0.49402499198913574 --maximum-depth 5727.9169921875`

When you run the command then it should ask for both your username and password, and will then install the data file in the current directory. This can take a moment as the filesize is around 250MB. 


## There needs to be compilers that are available for the GPU code for CUPy and so you need to then install nvhpc, which is best done through spack.

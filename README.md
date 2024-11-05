# GPU_Training_Course

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

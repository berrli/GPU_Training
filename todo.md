It will also likely be better for the poetry command to be ran with the use of poetry run download_data rather than asking people to use the actual command line arguement for copernicus since it is quite cumbersome.

# Tips and Tricks 

It it also worth mentioningt hat the common issues with the installation are likely to be related to the PATH or with some files being lft by spack within the .spack folder where the spack was initially downloaded

The steps taken to install python 3.12 with spack wer, and the issue was the presence of the .spack folder that has legacy environment. It is also a good idea to use a new environment name 
if things are getting confusing and messed up with legacy path elements. 



Mention the quirk of having to have two different types of python one for Spack and then one for the Poetry. It is just generally a good idea and anecdaotally saves hassle than having them point to the same thing. The spack python is used for CUDA. 
# Installation Instructions 

- git clone https://github.com/spack/spack.git
- source spack/share/spack/setup-env.sh
- spack env create cuda_course
- spack env activate -p cuda_course
- spack add python@3.12 
- spack add cuda
- spack spec
- spack install
- which python 
    This should then point to spack and so be something akin to 

You now want to install poetry itself which can be done with 
- curl -sSL https://install.python-poetry.org | python3 -

if there is an issue then you can uninstall it with 
- curl -sSL https://install.python-poetry.org | python3 - --uninstall

With poetry the final python packages, that are user level packages should now be installed. This can be done by navigating to the GitHub Training repo and then using `poetry install`.

You can then verify if the installation has been successfully by running `poetry run cuda_check` where you can then get the number of GPU devices. 
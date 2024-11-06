Create a spack environment that deals with the system level dependeices. This mean that both the python and the cuda needs to come from the spack environment. The goal for doing this it to make sure that the sudo access is not required for the platform

Create a poetry environment for the python level packages. The goal of this is to make the process of adding python packages easier. 

The main question is whether it is easier to get CUPy wih spack or peotry.

# Tips and Tricks 

It it also worth mentioningt hat the common issues with the installation are likely to be related to the PATH or with some files being lft by spack within the .spack folder where the spack was initially downloaded

The steps taken to install python 3.12 with spack wer, and the issue was the presence of the .spack folder that has legacy environment. It is also a good idea to use a new environment name 
if things are getting confusing and messed up with legacy path elements. 


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
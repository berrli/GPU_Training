Even when running GPU code with an interpreted language such as Python, you will still  need to engage with compilers due to the underlying code that is being ran. When running compiled code, [Spack](https://spack.io/) is highly recommened. 

You can download spack by running 

`git clone https://github.com/spack/spack.git`

You will then need to source spakc to add the ability to use it to the command line with:

`source spack/share/spack/setup-env.sh`

This will then add spack to your command line, that you can verify with:

`spack --version`

You will now want to create a new environment with

`spack env create gpu_training`

and activate the environment with 

`spack env activate -p gpu_training`

Of note is that spack is desegined to take into consideration compilers with the packages that are being created. The following goes over the particulars of spack commands, as the commands are similar to other package amnagers (such as Poetry, conda etc.) to be confusing similar but in a fundamental level work different. E.g. using add does not actually download the package that you are interested in.

# Spack Commands Overview

---

## `spack info`

- **Purpose**: Provides detailed information about a specific package.
- **Usage**: `spack info <package_name>`
- **Description**:
  - Displays metadata for a package, including:
    - Available versions
    - Variants (optional features or configuration options)
    - Dependencies
    - Compiler compatibility
  - Useful for understanding package configurations, choosing specific versions, and enabling or disabling variants before installation.
  
- **Example**:
  ```bash
  spack info python


## `spack add`

- **Purpose**: Adds a package to a Spack environment.
- **Usage**: `spack add <package_name>`
- **Description**: 
  - Adds a package to the current Spack environment’s configuration file without installing it.
  - Allows specifying versions and variants (e.g., `spack add <package_name>@<version> +<variant>`).
  
- **Example**:
  ```bash
  spack add python@3.9.6

## `spack spec`

- **Purpose**: Shows a detailed view of a package’s configuration.
- **Usage**: `spack spec <package_name>`
- **Description**:
  - Displays how Spack will interpret a package request, including dependencies, versions, and variants.
  - Useful for understanding how Spack resolves a package’s specifications before installation.

- **Example**:
  ```bash
  spack spec python@3.9.6

## `spack spec`

- **Purpose**: Shows a detailed view of a package’s configuration.
- **Usage**: `spack spec <package_name>`
- **Description**:
  - Displays how Spack will interpret a package request, including dependencies, versions, and variants.
  - Useful for understanding how Spack resolves a package’s specifications before installation.

- **Example**:
  ```bash
  spack spec python@3.9.6

## `spack concretize`

- **Purpose**: Ensures all dependencies are fully specified for a Spack environment.
- **Usage**: `spack concretize`
- **Description**:
  - Finalizes package versions, variants, and dependencies based on the environment’s specifications, preparing it for installation.
  - Resolves any ambiguities in the environment configuration to ensure compatibility across packages.

- **Example**:
  ```bash
  spack concretize


## `spack install`

- **Purpose**: Installs a package within the Spack environment.
- **Usage**: `spack install <package_name>`
- **Description**:
  - Downloads, builds, and installs the specified package, along with its dependencies.
  - Allows specifying versions and variants (e.g., `spack install <package_name>@<version> +<variant>`).
  - Can be used with flags such as `--fail-fast` to stop on the first error.

- **Example**:
  ```bash
  spack install gcc@10.2.0 +fortran


## `spack load`

- **Purpose**: Loads an installed package into the current environment.
- **Usage**: `spack load <package_name>`
- **Description**:
  - Modifies environment variables (e.g., `PATH`, `LD_LIBRARY_PATH`) to include the specified package.
  - Useful for making packages available in the shell without permanently adding them.
  - Allows loading specific versions (e.g., `spack load <package_name>@<version>`).

- **Example**:
  ```bash
  spack load python@3.9.6




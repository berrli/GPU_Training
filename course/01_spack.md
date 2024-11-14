
# Spack 

## Getting Started 

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

## Why Spack?

The core purpose of Spack is to simplify the building, installation, and management of software packages and their dependencies, particularly in the domain of complex scientific and high performance compuitng environments. The primary reasons for making use of Spack over other software are:
- **Handling of complex dependencies**: Spack is designed to handle complicated dependency trees, including multiple versions of the same library, specific compiler versions etc. For example, for a given functionality, one compiler performs considerably better than another. Spack makes creating an environment for each respective compiler easy, and mainly what it is designed for. 
- **Multiple Versions and Variants**: Further to support a number of different compiler versions, it can also support having a the same compiler but with different flags. For example it is possible that the compiler should use a particular type of offloading (discussed later on) or different types of floating point prevision, giving options for trade offs between speed and accuracy. 

These two points are the main draw of Spack and generally the primary reason for engaging with the software. However there are also a range of other reasons for engaging with Spack such as the ability to creat your own packages, apply patches and making custom repos with a number of different compilers, packages and other supporting elements. However these topics are outside of the scope of this course, but this is all functioanlity that exists within Spack which gives rise to its importance in HPC systems where very fine control over the software installed is needed. 

## Guided Tour of Spack

### Available Packages

To give a flavour of the different parts of Spack, the following commands provide an overview of the different parts of Spack. Assuming you are starting with a fresh spack environment, (e.g. `spack env create gpu_training` and ``spack env activate -p gpu_training`), then you may want to see the available packages, using 

`spack list`

By default there are a number of different packages, includig packages from both Python and R. Generally within Spack Python packages are prefixed with `py-`. 

### Adding Packages 

Say you wanted to add numpy to your spack environment then you could do so with 

`spack add py-numpy`

### Reading Proposed Installation Configuartions 

With the above command you have not specified any particular requirements for the version of numpy that you want to add. You can see all the dependencies and what would be installed in the current moment with the command:

`spack spec`

spack spec will provide you with the overall environment specification as it currently is. **NOTE: This is not what is currently installed but what would be installed if you executed `spack install`**. The tree that is returned has a number of different elements for you to consider. For example, before the package name you will see a number of different symbols including: 
- \- (Dash): The dash symbol indicates that the package is not installed on the system. Spack would build and install this packages as part of the installation process. 
- + (Plus): The plus symbol indicates that the package is already installed on the system. This package will be reused in the build process rather than rebuilt.
- e (External): The external symbol indictaes the package as an external dependency. Spack has detected that the package is available on the system outside of Spack own package managemne. This is often used for core system libraries, compilers or large packages that are difficult or unncessary to rebuild (such as glibc, cuda, particular mpi implementation)
Within spack you do have the option to overwrite alot of these elements, by specifying your own package specification, but again this is outside the scope of this course.

The second element of the `spack spec` output are the different package definiteitions. 

In Spack, the general form of a package specification includes elements such as the package name, version, compiler, compiler version, build options, variants, and target architecture, with the general structure of: 
`<package-name>@<version>%<compiler>@<compiler-version> build_system=<build-system> patches=<patch-id> arch=<platform>-<os>-<target>`

#### Breakdown of Components

`<package-name>`
The name of the package you want to install or manage (e.g., py-numpy, openblas, gcc).

`@<version>`
The version of the package. This can be a specific version (e.g., 2.1.2) or a version range, depending on the Spack specification.


`%<compiler>`
The compiler that Spack will use to build the package. The % symbol indicates the compiler selection. <compiler> could be gcc, intel, clang, etc.

`@<compiler-version>`
The version of the compiler specified. This follows the %<compiler> portion, indicating the exact compiler version (e.g., 11.4.1).

`build_system=<build-system>`
Specifies the build system or method Spack will use to build the package. Common build systems include python_pip, cmake, autotools, etc.

`patches=<patch-id>`
Indicates patches that Spack will apply to the package during installation. The patch-id is typically a unique hash or identifier for each patch.

`arch=<platform>-<os>-<target>`
arch specifies the architecture, operating system, and target platform.
- `<platform>` is usually linux, darwin (for macOS), or other OS platforms.
- `<os>` specifies the operating system or distribution, such as rhel9 (Red Hat Enterprise Linux 9) or ubuntu20.04.
- `<target>` specifies the CPU or hardware architecture, like zen2 (AMD), haswell (Intel), or arm.

#### Optional Elements
Variants: Additional options or configuration flags for the package, such as +mpi to enable MPI support or ~shared to disable shared libraries.
Custom Options: Some specifications may include additional flags or custom options (e.g., threads=none, symbol_suffix=none).

Here’s an example that includes variants and other custom options:

`openblas@0.3.18%gcc@10.2.0+fortran+pic threads=none build_system=makefile arch=linux-ubuntu20.04-haswell`


#### Example Package Overview
Given a specification such as:
py-numpy@2.1.2%gcc@11.4.1 build_system=python_pip patches=873745d arch=linux-rhel9-zen2
Package name: py-numpy
Version: 2.1.2
Compiler: gcc
Compiler version: 11.4.1
Build system: python_pip
Patch ID: 873745d
Architecture:
Platform: linux
OS: rhel9
Target: zen2
This form provides all the details Spack needs to configure, build, and install the package according to the specified parameters.


#### Package Dependeices 
The final element to understand for the `spack spec` is the use of the symbol `^`, which indicates a package dependency that also needs to be installed. For example in the following code snippet, py-numpy depends on gcc-runtime and glibc. 

```
 -   py-numpy@2.1.2%gcc@11.4.1 build_system=python_pip patches=873745d arch=linux-rhel9-zen2
[+]      ^gcc-runtime@11.4.1%gcc@11.4.1 build_system=generic arch=linux-rhel9-zen2
[e]      ^glibc@2.34%gcc@11.4.1 build_system=autotools arch=linux-rhel9-zen2
```

#### Changing the spec

Up to this point we havnt installed anything within our environment, and so we are free to iterate and makes changes, reviewing the spec to see the changes that have been made. At this point you have made a mistake and want to run legacy code that doesnt run with Numpy 2.x but rather needs to use Numpy 1.x. Using the following we can specify we want to use a numpy 1.x package. 

`spack add py-numpy@1.26`

If you were now to use `spack spec` again you will see that the proposed specification has changed, with NumPy 1.26 being proposed. 

### Installing Packages

Once you are happy with the proposed specification you can install all of the required packages with:

`spack install`

After the instalation process has completed the relevant packages should now be available for use. 


### Deactivate Environment 

You can deactivate the environment by using 

`spack env deactivate`


# Spack Commands Cheat Sheet

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




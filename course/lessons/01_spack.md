
# Spack 

## Getting Started 

Even when running GPU code with an interpreted language such as Python, you will still  need to engage with compilers due to the underlying code that is being ran. When running compiled code, [Spack](https://spack.io/) is highly recommened. 

You can download spack by running 

``` bash
git clone https://github.com/spack/spack.git
```

You will then need to source spakc to add the ability to use it to the command line with:

``` bash
source spack/share/spack/setup-env.sh
```

This will then add spack to your command line, that you can verify with:

``` bash
spack --version
```

You will now want to create a new environment with

``` bash
spack env create gpu_training
```

and activate the environment with 

``` bash
spack env activate -p gpu_training
```

Of note is that spack is desegined to take into consideration compilers with the packages that are being created. The following goes over the particulars of spack commands, as the commands are similar to other package amnagers (such as Poetry, conda etc.) to be confusing similar but in a fundamental level work different. E.g. using add does not actually download the package that you are interested in.

## Why Spack?

The core purpose of Spack is to simplify the building, installation, and management of software packages and their dependencies, particularly in the domain of complex scientific and high-performance computing environments. The primary reasons for making use of Spack over other software are:

- **Handling of complex dependencies**: Spack is designed to handle complicated dependency trees, including multiple versions of the same library, specific compiler versions, etc. For example, for a given functionality, one compiler may perform considerably better than another. Spack makes creating an environment for each respective compiler easy, and this is mainly what it is designed for.

- **Multiple Versions and Variants**: In addition to supporting different compiler versions, Spack can also manage the same compiler with different flags. For example, the compiler could use a specific type of offloading (discussed later on) or different levels of floating-point precision, allowing for trade-offs between speed and accuracy.


These two points are the main draw of Spack and generally the primary reason for engaging with the software. However there are also a range of other reasons for engaging with Spack such as the ability to creat your own packages, apply patches and making custom repos with a number of different compilers, packages and other supporting elements. However these topics are outside of the scope of this course, but this is all functioanlity that exists within Spack which gives rise to its importance in HPC systems where very fine control over the software installed is needed. 

## Guided Tour of Spack

### Available Packages

To give a flavour of the different parts of Spack, the following commands provide an overview of the different parts of Spack. Assuming you are starting with a fresh spack environment, (e.g. `spack env create gpu_training` and ``spack env activate -p gpu_training`), then you may want to see the available packages, using 

``` bash
spack list
```

By default there are a number of different packages, includig packages from both Python and R. Generally within Spack Python packages are prefixed with `py-`. 

### Adding Packages 

Say you wanted to add numpy to your spack environment then you could do so with 

``` bash
spack add py-numpy
```

### Reading Proposed Installation Configuartions 

With the above command you have not specified any particular requirements for the version of numpy that you want to add. You can see all the dependencies and what would be installed in the current moment with the command:

``` bash
spack spec
```

`spack spec` will provide you with the overall environment specification as it currently is. **NOTE: This is not what is currently installed but what would be installed if you executed `spack install`.** The tree that is returned has a number of different elements for you to consider. For example, before the package name you will see a number of different symbols, including:

- **`-` (Dash)**: The dash symbol indicates that the package is not installed on the system. Spack would build and install this package as part of the installation process.

- **`+` (Plus)**: The plus symbol indicates that the package is already installed on the system. This package will be reused in the build process rather than rebuilt.

- **`e` (External)**: The external symbol indicates the package is an external dependency. Spack has detected that the package is available on the system outside of Spack’s own package management. This is often used for core system libraries, compilers, or large packages that are difficult or unnecessary to rebuild (such as `glibc`, `cuda`, or a particular MPI implementation).

Within Spack, you do have the option to override many of these elements by specifying your own package specification, but this is outside the scope of this course.

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

``` bash
 -   py-numpy@2.1.2%gcc@11.4.1 build_system=python_pip patches=873745d arch=linux-rhel9-zen2
[+]      ^gcc-runtime@11.4.1%gcc@11.4.1 build_system=generic arch=linux-rhel9-zen2
[e]      ^glibc@2.34%gcc@11.4.1 build_system=autotools arch=linux-rhel9-zen2
```

#### Changing the spec

Up to this point we havnt installed anything within our environment, and so we are free to iterate and makes changes, reviewing the spec to see the changes that have been made. At this point you have made a mistake and want to run legacy code that doesnt run with Numpy 2.x but rather needs to use Numpy 1.x. Using the following we can specify we want to use a numpy 1.x package. 

``` bash
spack add py-numpy@1.26
```

If you were now to use `spack spec` again you will see that the proposed specification has changed, with NumPy 1.26 being proposed. 

### Installing Packages

Once you are happy with the proposed specification you can install all of the required packages with:

``` bash
spack install
```

After the instalation process has completed the relevant packages should now be available for use. 


### Deactivate Environment 

You can deactivate the environment by using 

``` bash
spack env deactivate
```




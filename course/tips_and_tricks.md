
# Tips and Tricks

Programming GPUs can be pretty complex, particularly during the set-up phase, where a number of different drivers are required to run code on the GPU. This section provides some potential lines of inquiry as to what may be causing issues with your current set-up if you are entirely stuck based on personal past experiences of common faults. 

## PATH
In UNIX, **PATH** is an environment variable listing directories to search for commands. If a command isn’t found, it’s likely the directory containing it isn’t in PATH. However, due to the number of different versions of software used in these projects, such as having the same package compiled with different compilers, e.g. GCC for OpenMP or NVHPC-related compilers for OpenACC, then a misconfigured PATH can be a common cause of issues. The use of `which <command>` will help you to identify what is being run when you use that line on the command line. You can see this clearly within this project, where there is a python used by spack and then also a python used by poetry, where they share the same version, but their distinguishing factor is where they are located in regards to the file path. 

## Starting Fresh 

Sometimes, with the number of different elements involved in a GPU project, it can be helpful to clean the workspace and start fresh. To remove spack, you will also need to remove the `.spack` directory alongside the `spack` directory. If you don't remove the hidden directory and then simply clone the spack repo again, then you may find that the issue with the spack might be persistent from elements left in the hidden directory. 
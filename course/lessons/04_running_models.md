# Leaveaging GPUs

## Pseudocode

The psuedocode that implements the diffusion loop is: 

``` plaintext
1. For each timestep from 1 to num_timesteps:
   2. Copy the current temperature values to a temporary array (temp_copy)
   3. Initialize arrays for neighbor sums and neighbor counts with zeros
   4. For each valid cell (ignoring boundaries):
      5. Calculate the sum of neighboring cells:
         - Add the value of the front neighbor if valid
         - Add the value of the back neighbor if valid
         - Add the value of the left neighbor if valid
         - Add the value of the right neighbor if valid
         - Add the value of the top neighbor if valid
         - Add the value of the bottom neighbor if valid
      6. Count the number of valid neighbors for each direction
   7. Update the cell's temperature:
      - New temperature = current temperature + diffusion coefficient * (neighbor_sum - 6 * current temperature) / neighbor_count
   8. Ensure invalid points (NaN) remain unchanged
   9. Update the main temperature array with the new values
```

## Running with NumPy 

``` bash 
poetry run diffusion_numpy --num_timesteps 100
```

The above command will run the 3D diffusion model using the NumPy version of the code for 100 timesteps. Once the execution has finished then a report will be provided concerning the time taken for execution. When running on an AMD EPYC 7552 48-Core Processor, the execution outputs:

``` plaintext 
NumPy model completed in 489.2647 seconds. Average time per timestep: 4.8926 seconds.
```

You can visualise the model outputs producded with 

``` bash 
poetry run visualise_slice --target_depth 0 --animation_speed 100 --data_file predicted_temperatures_numpy.nc 
```

Of note is that the file `predicted_temperatures_numpy.nc` is generated during the execution of the above command for the script `diffusion_numpy`. This will then generate a new interactive HTML file `output/predicted_temperature_2d_interactive.html`.


## Running With CuPy

As the same code has been wrote in CuPy you can experiment with the difference between CPU and GPU code with the following:

``` bash 
poetry run diffusion_cupy --num_timesteps 100
```

The above command will run the 3D diffusion model using the CuPy version of the code for 100 timesteps. Once the execution has finished then a report will be provided concerning the time taken for execution. When running on an NVIDIA A40 GPU, the execution outputs:

``` plaintext 
CuPy model completed in 171.9884 seconds. Average time per timestep: 1.7199 seconds.
```

You can visualise the model outputs producded with 

``` bash 
poetry run visualise_slice --target_depth 0 --animation_speed 100 --data_file predicted_temperatures_cupy.nc 
```

Of note is that the file `predicted_temperatures_numpy.nc` is generated during the execution of the above command for the script `diffusion_numpy`. This will then generate a new interactive HTML file `output/predicted_temperature_2d_interactive.html`.

## Performance Comparison: CPU vs GPU

### Overall Speedup
- **CPU runtime**: 489 seconds  
- **GPU runtime**: 171.9884 seconds  
- **Speedup factor**:  
  \[
  \text{Speedup} = \frac{\text{CPU time}}{\text{GPU time}} = \frac{489}{171.9884} \approx 2.84
  \]  
  The GPU completed the task approximately 2.84 times faster than the CPU.

### Per-Timestep Speedup
- **CPU average timestep**: 4.9 seconds  
- **GPU average timestep**: 1.7199 seconds  
- **Speedup factor per timestep**:  
  \[
  \text{Speedup per timestep} = \frac{\text{CPU timestep}}{\text{GPU timestep}} = \frac{4.9}{1.7199} \approx 2.85
  \]  
  On a per-timestep basis, the GPU is about 2.85 times faster.

### Efficiency Observation
- The consistent speedup factor (both overall and per timestep) suggests that the GPU effectively parallelizes computations without significant overhead from data transfer or kernel launches.

### Implications
- **Computational Efficiency**:  
  Using a GPU provides substantial performance gains, especially for tasks with repetitive, parallelizable computations such as numerical modeling or simulations.
- **Observed Speedup** (~2.84x improvement) suggests:  
  - The task is well-suited for GPU acceleration.  
  - Full potential of the GPU might not yet be realized due to:
    - Limited parallelism in the workload.  
    - Overheads from memory transfers between CPU and GPU.  
    - Suboptimal use of GPU-specific optimizations.

The GPU's performance significantly outpaces the CPU for this task, reducing runtime by approximately 65%. Of note is that this approach is simply a direct move from NumPy to CuPy which represents a minimal amount of effort. Further optimization of the GPU code could enhance performance and exploit its full potential, leveraging on known time intensive tasks for GPUs such as data transfer. 

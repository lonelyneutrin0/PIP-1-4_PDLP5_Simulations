# PIP-1-4_PDLP5_Simulations (Single Lipid Bilayer)
This directory contains the builds and scripts used for the single lipid bilayer aquaporin simulations. The simulation data can be found at `/serviceberry/tank/hkbel/PIP-1-4_PDLP5_Simulations/singlebilayer/sims`. 

## Project Structure 
```txt
/singlebilayer/ 
├──builds
|  ├──porinalone
|  |   ├──grad
|  |   |  ├──0.010
|  |   |  ├──0.150
|  |   |  ├──1.0
|  |   ├──nograd
|  |   |  ├──0.010
|  |   |  ├──0.150
|  |   |  ├──1.0
|  ├──porinwithcap
|  |   ├──grad
|  |   |  ├──0.010
|  |   |  ├──0.150
|  |   |  ├──1.0
|  |   ├──nograd
|  |   |  ├──0.010
|  |   |  ├──0.150
|  |   |  ├──1.0
|
├──scripts
|  ├──build_scripts
|  ├──sim_scripts
|
├──sims
|  ├──NPT
|  |  ├──porinalone
|  |  |   ├──grad
|  |  |   |  ├──0.010
|  |  |   |  ├──0.150
|  |  |   |  ├──1.0
|  |  |   ├──nograd
|  |  |   |  ├──0.010
|  |  |   |  ├──0.150
|  |  |   |  ├──1.0
|  |  ├──porinwithcap
|  |  |   ├──grad
|  |  |   |  ├──0.010
|  |  |   |  ├──0.150
|  |  |   |  ├──1.0
|  |  |   ├──nograd
|  |  |   |  ├──0.010
|  |  |   |  ├──0.150
|  |  |   |  ├──1.0
|  |
|  ├──NVT
|  |  ├──porinalone
|  |  |   ├──grad
|  |  |   |  ├──0.010
|  |  |   |  ├──0.150
|  |  |   |  ├──1.0
|  |  |   ├──nograd
|  |  |   |  ├──0.010
|  |  |   |  ├──0.150
|  |  |   |  ├──1.0
|  |  ├──porinwithcap
|  |  |   ├──grad
|  |  |   |  ├──0.010
|  |  |   |  ├──0.150
|  |  |   |  ├──1.0
|  |  |   ├──nograd
|  |  |   |  ├──0.010
|  |  |   |  ├──0.150
|  |  |   |  ├──1.0
|
├──data
|  ├──porinalone
|  |   ├──grad
|  |   |  ├──0.010
|  |   |  ├──0.150
|  |   |  ├──1.0
|  |   ├──nograd
|  |   |  ├──0.010
|  |   |  ├──0.150
|  |   |  ├──1.0
|  ├──porinwithcap
|  |   ├──grad
|  |   |  ├──0.010
|  |   |  ├──0.150
|  |   |  ├──1.0
|  |   ├──nograd
|  |   |  ├──0.010
|  |   |  ├──0.150
|  |   |  ├──1.0
|
├──toppar
```
## Builds 
The `builds` subdirectory contains the protein files used for simulation. There are 2 subdirectories - 
- `porinalone`: Uncapped aquaporin files 
- `porinwithcap`: Capped aquaporin files

In each of these, there are two folders: 
- `grad`: Files with a gradient, i.e. all sodium ions moved to the top compartment, with equal chlorides in both compartments
- `nograd`: Files with no gradient, i.e. equal number of sodium ions and chloride ions in both compartments

There are protein files with 10mM, 150mM, and 1M ion concentrations.

## Scripts 
This directory contains various scripts used to perform calculations or load trajectories. The packages assumed to be installed are `numpy` and `matplotlib`.

### `calc_ions.tcl `
This script calculates the z-coordinate of each ion for each frame of a given trajectory. It assumes that all required `.dcd` files are already loaded. The outputs are `cation_z.dat` and `anion_z.dat`, which contain the data in the form `frame z_1 z_2 ....`.

### `epot.tcl` 
This script calls [PMEPot](https://www.ks.uiuc.edu/Research/vmd/plugins/pmepot/) and creates a potential map of a given trajectory. It assumes that all required `.dcd` files are already loaded into VMD. The potential values are stored in the file `epot.dx`. 

### `load.tcl `
This is a utility script to load `.dcd` files into VMD. It assumes that the `.psf` file is already loaded, and that the trajectory files are located in the directory in which the script call occurs.

### `new_griddata.py` 
This script creates a placeholder `potential.dx` file, which is required for gridforces simulations. Note that certain lines of the file have to be modified depending on the periodic cell dimensions of the given system.

```py
shape = (2, 2, periodic_z_length+10) # ADD 10A TO THE PERIODIC CELL Z LENGTH
origin = np.array([o_x, o_y, o_z]) # ADD THE ORIGIN OF THE PERIODIC CELL HERE
```

### `potential.py `
This script converts the `epot.dx` file produced by `epot.tcl` and produces a potential-z coordinate plot. It assumes that `.dx` file is present in the directory in which the script call occurs. The plot and plot data are saved to `plot.png` and `z_potential.dat`. 

### `reduce.tcl`
This script is used to reduce the number of ions in a given `pdb` file. The number of ions to reduce should be modified. 
```py
set sod_to_delete [lrange $sodium_indices 0 n-1]
set cla_to_delete [lrange $chloride_indices 0 m-1]
```
The output `psf` and `pdb` files are `system.psf` and `system.pdb`.

### `create_grad.tcl`
This script is used to write `grad.pdb` files, which are required for gridforces. 

### `plot_ion_distribution.py`
This script takes a `cation_z.dat` and `anion_z.dat` file produced by `calc_ions.tcl` and plots a histogram of ion distribution over the second half of the trajectory. It assumes that the `.dat` files are located in the directory in which the function call occurs. The following lines should be modified depending on the system size. 
```py
Z_MAX = 85 
Z_MIN = -85 
BIN_SIZE = 5
```

### `single_trackwater.py`
This file loads the `.psf` and trajectory files in the current directory and tracks water molecule positions through the aquaporin. It saves them to a compressed `.npy` file.

Note: Run this through VMD's Python interpreter

### `single_plotwater.py`
This file takes the `.npy` file produced by `trackwater.py` and bins the water positions to track crossings through the aquaporin. 

Note: Currently, this sums all crossings and does not account for direction, see #2.

### `trackwater.py`
This is a master script for tracking water molecules across all systems, and multiple replicates. It expects the file system to be identical to the abovementioned project structure.

Note: Run this through VMD's Python interpreter.

### `plotwater.py`
This is a master script for calculating crossing rates across all systems, and multiple replicates. It expects the file system to be identical to the abovementioned project structure. 

Note: This file prints output, so it's advisable to redirect it with something like `python plotwater.py > analysis.log`

### `analysis.sh`
This is a master bash script that just calls `trackwater.py` and `plotwater.py` and directs the output to a log file. 

Note: This script must be modified to activate the desired virtual environment.

## Simulations 
The `sims` directory contains `run.namd` files to run the simulations. All required files have been included in `builds`. Since GitHub does not support very large files in repositories, existing simulation data should be copied from `/serviceberry/tank/hkbel/PIP-1-4_PDLP5_Simulations/singlebilayer/sims`.
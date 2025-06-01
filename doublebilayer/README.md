# PIP-1-4_PDLP5_Simulations (Double Lipid Bilayer)
This directory contains the builds and scripts used for the double lipid bilayer aquaporin simulations. The simulation data can be found at `/serviceberry/tank/hkbel/PIP-1-4_PDLP5_Simulations/doublebilayer/sims`

## File Structure
```txt
/doublebilayer/ 
├──builds
|  ├──porinalone
|  |   ├──ionized_throughout/0.150
|  |   ├──ionized_inside
|  |   |  ├──0.010
|  |   |  ├──0.036
|  |   |  ├──0.150
|  |   ├──ionized_outside
|  |   |  ├──0.010
|  |   |  ├──0.036
|  |   |  ├──0.150
|  |   ├──cations_outside/0.010
|  |   ├──cations_inside/0.010
|  |   ├──misc
|  |   |  ├──noions/0.010
|  |   |  ├──nograd/0.150
|  ├──porinwithcap
|  |   ├──ionized_inside
|  |   |  ├──0.010
|  |   |  ├──0.036
|  |   |  ├──0.150
|  |   ├──ionized_outside
|  |   |  ├──0.010
|  |   |  ├──0.036
|  |   |  ├──0.150
|  |   ├──cations_outside/0.010
|  |   ├──cations_inside/0.010
|
├──scripts
|
├──sims
|  ├──porinalone
|  |   ├──ionized_throughout/0.150
|  |   ├──ionized_inside
|  |   |  ├──0.010
|  |   |  ├──0.036
|  |   |  ├──0.150
|  |   ├──ionized_outside
|  |   |  ├──0.010
|  |   |  ├──0.036
|  |   |  ├──0.150
|  |   ├──cations_outside/0.010
|  |   ├──cations_inside/0.010
|  ├──porinwithcap
|  |   ├──ionized_inside
|  |   |  ├──0.010
|  |   |  ├──0.036
|  |   |  ├──0.150
|  |   ├──ionized_outside
|  |   |  ├──0.010
|  |   |  ├──0.036
|  |   |  ├──0.150
|  |   ├──cations_outside/0.010
|  |   ├──cations_inside/0.010
|
├──toppar
```

## Builds 
The `builds` subdirectory contains the protein files used for simulation. There are 2 subdirectories - 
- `porinalone`: Uncapped aquaporin files 
- `porinwithcap`: Capped aquaporin files 

In each of these, there are four folders: 
- `ionized_inside`: All ions moved to the "inner" compartment. 
- `ionized_outside`: All ions moved to the "outer" compartment. 
- `cations_inside`: All cations moved to the inner compartment, and all anions moved to the outer compartment.
- `cations_outside`: All cations moved to the outer compartment, and all anions moved to the inner compartment. 


There are protein files with 10mM, 36mM and 150mM ion concentrations. There are also some miscellaneous builds that were used for testing, in the `misc` folder.


## Scripts 
This directory contains various scripts used to perform calculations or load trajectories. The packages assumed to be installed are `numpy` and `matplotlib`.

### `calc_ions.tcl `
This script calculates the z-coordinate of each ion for each frame of a given trajectory. It assumes that all required `.dcd` files are already loaded. The outputs are `cation_z.dat` and `anion_z.dat`, which contain the data in the form `frame z_1 z_2 ....`.

### `epot.tcl` 
This script calls [PMEPot](https://www.ks.uiuc.edu/Research/vmd/plugins/pmepot/) and creates a potential map of a given trajectory. It assumes that all required `.dcd` files are already loaded into VMD. The potential values are stored in the file `epot.dx`. 

### `load.tcl `
This is a utility script to load `.dcd` files into VMD. It assumes that the `.psf` file is already loaded, and that the trajectory files are located in the directory in which the script call occurs.

### `potential.py `
This script converts the `epot.dx` file produced by `epot.tcl` and produces a potential-z coordinate plot. It assumes that `.dx` file is present in the directory in which the script call occurs. The plot and plot data are saved to `plot.png` and `z_potential.dat`. 

### `reduce.tcl`
This script is used to reduce the number of ions in a given `pdb` file. The number of ions to reduce should be modified. 
```py
set sod_to_delete [lrange $sodium_indices 0 n-1]
set cla_to_delete [lrange $chloride_indices 0 m-1]
```
The output `psf` and `pdb` files are `system.psf` and `system.pdb`.

## Simulations 
The `sims` directory contains `run.namd` files to run the simulations. All required files have been included in `builds`. Since GitHub does not support very large files in repositories, existing simulation data should be copied from `/serviceberry/tank/hkbel/PIP-1-4_PDLP5_Simulations/doublebilayer/sims`.

Most subdirectories are labelled `0`, `1`, `2` for the run number. There are two exceptions - `NVT` indicates an NVT MD sim, and `PistonParam` is an `NPT` MD sim with different Langevin piston parameters.
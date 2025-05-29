# PIP-1-4_PDLP5_Simulations (Single Lipid Bilayer)
This directory contains the builds and scripts used for the single lipid bilayer aquaporin simulations. The simulation data can be found at `/serviceberry/tank/hkbel/aquaporin/singlebilayer/sims/gridforces`. 

## Builds 
The `builds` subdirectory contains the protein files used for simulation. There are 2 subdirectories - 
- `porinalone`: Uncapped aquaporin files 
- `porinwithcap`: Capped aquaporin files (currently empty as testing is being done with the uncapped aquaporin)

In each of these, there are two folders: 
- `grad`: Files with a gradient, i.e. all sodium ions moved to the top compartment
- `nograd`: Files with no gradient, i.e. equal number of sodium ions and chloride ions in both compartments

There are protein files with 10mM and 150mM ion concentrations. `grad_T2.pdb` is used for gridforces. 
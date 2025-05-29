mol new system.psf
mol addfile system.pdb

set sel [atomselect top all]
set cation [atomselect top "resname SOD"]
set anion [atomselect top "resname CLA"]
set ions [atomselect top ions]

$sel set occupancy 1
$cation set occupancy 1
$anion set occupancy -1

$sel set beta 0
$ions set beta 5

$sel writepdb gradT_2.pdb
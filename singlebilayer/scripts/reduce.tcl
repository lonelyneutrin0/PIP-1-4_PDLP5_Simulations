set sodiums [atomselect top "resname SOD"]

set chlorides [atomselect top "resname CLA"]

set sodium_indices [$sodiums get index]

set chloride_indices [$chlorides get index]

set sod_to_delete [lrange $sodium_indices 0 195]

set cla_to_delete [lrange $chloride_indices 0 195]

set to_delete [concat $sod_to_delete $cla_to_delete]

set remaining [atomselect top "not index [join $to_delete]"]

$remaining writepsf system.psf
$remaining writepdb system.pdb



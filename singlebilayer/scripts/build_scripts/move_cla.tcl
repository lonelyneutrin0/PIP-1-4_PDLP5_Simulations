set chlorides [atomselect top "resname CLA and z<0"]

set indices [$chlorides get index]

set move_indices [lrange $indices 0 30]

set sel [atomselect top "index [join $move_indices]"]

$sel moveby {0 0 10}
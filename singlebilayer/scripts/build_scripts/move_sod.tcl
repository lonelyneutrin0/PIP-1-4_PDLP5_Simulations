set sodiums [atomselect top "resname SOD and (z<-90 and z>-100)"]

set indices [$sodiums get index]

set move_indices [lrange $indices 0 72]

set sel [atomselect top "index [join $indices]"]

$sel moveby {0 0 10}
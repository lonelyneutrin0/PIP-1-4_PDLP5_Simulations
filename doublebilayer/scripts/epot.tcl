# TCL Script to get electric potential of a system using PMEPot 

package require pmepot

set all [atomselect top all]

set molid 0 

set o [molinfo $molid get center]
set a [molinfo $molid get a]
set b [molinfo $molid get b]
set c [molinfo $molid get c]

set a_list [list $a 0 0]
set b_list [list 0 $b 0]
set c_list [list 0 0 $c]

set basis_list [list [lindex $o 0]  $a_list $b_list $c_list]

pmepot -sel $all -frames all -cell $basis_list -dxfile epot.dx -ewaldfactor 0.25
#pmepot -sel $all -cell $basis_list -dxfile epot.dx -ewaldfactor 0.25

# Appearance
# set molid [molinfo top get id]

# mol modcolor 0 $molid Volume 0

# mol modstyle 0 $molid VolumeSlice Z 0.5

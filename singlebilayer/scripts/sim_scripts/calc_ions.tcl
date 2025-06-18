set numframes [molinfo top get numframes]

set cation [atomselect top "resname SOD"]
set anion  [atomselect top "resname CLA"]

set cation_indices [$cation get index]
set anion_indice [$anion get index]

set file1 [open "cation_z.dat" w]
set file2 [open "anion_z.dat" w]

for { set i 0}  {$i < $numframes} {incr i} {
    $cation frame $i
    $anion frame $i
    $cation update
    $anion update
    
    set z1 [$cation get z]
    set z2 [$anion get z]
    
    puts $file1 [format "%d \t %s " $i $z1]
    puts $file2 [format "%d \t %s " $i $z2] 
}

close $file1
close $file2
exit

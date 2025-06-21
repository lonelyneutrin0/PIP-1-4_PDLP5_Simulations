## Run it by: source solvation.tcl in VMD's TkConsole ##
## Auto-detects membrane region using segname MEMB and solvates above and below ##
## Outputs box dimensions to file, adds ions, and prepares solvated structure ##

set conc 0.50  ;# Replace or extend this list with your system indices (or just use 1 entry)
set xysize 140 
set zsize 166

set input_file "noions"

# Load input structure
mol load psf ${input_file}.psf pdb ${input_file}.pdb

set allsel [atomselect top all]
set all_minmax [measure minmax $allsel]
set x1 [lindex [lindex $all_minmax 0] 0]
set x2 [lindex [lindex $all_minmax 1] 0]
set y1 [lindex [lindex $all_minmax 0] 1]
set y2 [lindex [lindex $all_minmax 1] 1]

# Set solvation box dimensions in XY
set x1 [expr { -$xysize / 2.0 }]
set x2 [expr {  $xysize / 2.0 }]
set y1 [expr { -$xysize / 2.0 }]
set y2 [expr {  $xysize / 2.0 }]

# Auto-detect membrane Z boundaries
set membsel [atomselect top "segname MEMB"]
set memb_minmax [measure minmax $membsel]
set memb_z1 [lindex [lindex $memb_minmax 0] 2]
set memb_z2 [lindex [lindex $memb_minmax 1] 2]

set memb_length [expr {$memb_z2 - $memb_z1}]
set buffer [expr {($zsize - $memb_length)/2}] ;# Amount of water (in Å) above/below the membrane

# Cleanup before solvation
mol delete all

## ---- Solvation ---- ##
package require solvate

# Solvate below the membrane
solvate ${input_file}.psf ${input_file}.pdb \
    -minmax [list [list $x1 $y1 [expr {$memb_z1 - $buffer}]] [list $x2 $y2 [expr {$memb_z1+2}]]] \
    -o lower_water

# Solvate above the membrane
solvate lower_water.psf lower_water.pdb \
    -minmax [list [list $x1 $y1 [expr {$memb_z2-2}]] [list $x2 $y2 [expr {$memb_z2 + $buffer}]]] \
    -o with_water -s WA

mol delete all

## ---- Autoionization ---- ##
package require autoionize
if {$conc == 0} {
    autoionize -psf with_water.psf -pdb with_water.pdb -cation SOD -anion CLA -seg ION -o ionize -neutralize
} else {
    autoionize -psf with_water.psf -pdb with_water.pdb -sc $conc -cation SOD -anion CLA -seg ION -o ionize
}

mol delete all

## ---- Set up PBC box ---- ##
mol new ionize.psf
mol addfile ionize.pdb
set sel1 [atomselect top all]
set minmax [measure minmax $sel1]
set min [lindex $minmax 0]
set max [lindex $minmax 1]
set xsize [expr abs([lindex $min 0]) + abs([lindex $max 0])]
set ysize [expr abs([lindex $min 1]) + abs([lindex $max 1])]
set zsize [expr abs([lindex $min 2]) + abs([lindex $max 2])]
pbc set [list $xsize $ysize $zsize] -all -molid top

## ---- Save Final Structure ---- ##
$sel1 writepdb system.pdb
$sel1 writepsf system.psf
mol delete all

## ---- Save Box Info ---- ##
mol new system.psf
mol addfile system.pdb
set sel2 [atomselect top all]
set center [measure center $sel2]
set outfile [open "box_size.txt" w]
puts $outfile [format "cellBasisVector1 %2.2f 0 0 "  $xsize ]
puts $outfile [format "cellBasisVector2 0 %2.2f 0 "  $ysize ]
puts $outfile [format "cellBasisVector3 0 0 %2.2f "  $zsize ]
puts $outfile "cellOrigin 0 0 0"
puts $outfile "Total Charge on System: [eval vecadd [$sel2 get charge]]"
close $outfile

pbc box -color orange -style tubes -width 1 -center bb
mol delete all
resetpsf

## ---- Clean Temporary Files ---- ##
file delete with_water.pdb with_water.psf with_water.log
file delete ionize.pdb ionize.psf
file delete lower_water.pdb lower_water.psf lower_water.log

exit

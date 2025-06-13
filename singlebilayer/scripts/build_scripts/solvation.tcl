 ## run it by " source solvation.tcl " in tkconsole ##
 ## do remember to make the psf and filename to system_autopsf ##
 ## creating the logfile and an outfile to store box vectors ## 
 ##logfile logfile.txt
set ICs {0.50}

foreach IC $ICs {
mol load psf memb_lig_${IC}.psf pdb memb_lig_${IC}.pdb
set memb [atomselect top all]
set minmax [measure minmax $memb]
set min [lindex $minmax 0]
set max [lindex $minmax 1]

set x1 [lindex $min 0]
set x2 [lindex $max 0]
set y1 [lindex $min 1]
set y2 [lindex $max 1]
set z1 [lindex $min 2]
set z2 [lindex $max 2]

set xysize 80
set x1 [expr { -$xysize / 2}]
set x2 [expr { $xysize / 2}]
set y1 [expr { -$xysize / 2}]
set y2 [expr { $xysize / 2}]
set zsize 100
set z1 [expr { -$zsize / 2}]
set z2 [expr { $zsize / 2}]
mol delete all
set outfile [open "box_size.txt" w ]
 
 #puts "Enter the file name **INCLUDE CHARACTERS BEFORE _autopsf"
 #set filex [gets stdin]
 set filex "memb_lig_${IC}"
 puts "****************************"
 puts $filex
 #puts "Enter Salt Concentration"
 #set salt [gets stdin]
 set salt 0.15
 ## solvating the file ##
 package require solvate
 solvate ${filex}.psf ${filex}.pdb -minmax [list [list $x1 $y1 [expr $z1 +10]] [list $x2 $y2 -22]] -o half_water
 solvate half_water.psf half_water.pdb -minmax [list [list $x1 $y1 22] [list $x2 $y2 [expr $z2+10]]] -o with_water -s WA
 mol delete all
 ## adding ions to neutralize the system ##
 package require autoionize
 if {$salt==0} {
 autoionize -psf with_water.psf -pdb with_water.pdb -cation SOD -anion CLA -seg ION -o ionize -neutralize 
 } else {
 autoionize -psf with_water.psf -pdb with_water.pdb -sc ${salt} -cation SOD -anion CLA -seg ION -o ionize 
 }
 # either use -> -sc ${salt} or -neutralize
 mol delete all
 ## setting up the box ##
 mol new ionize.psf
 mol addfile ionize.pdb
 set sel1 [atomselect top all]

 set minmax [measure minmax $sel1]
 set min [lindex $minmax 0]
 set max [lindex $minmax 1]
 set x1 [lindex $min 0]
 set x2 [lindex $max 0]
 set y1 [lindex $min 1]
 set y2 [lindex $max 1]
 set z1 [lindex $min 2]
 set z2 [lindex $max 2]
 set xsize [expr abs($x1)+abs($x2)]
 set ysize [expr abs($y1)+abs($y2)]
 #$sel1 moveby [list [expr -1*$x1] [expr -1*$y1] [expr -1*$z1]]
 pbc set [list [expr abs($x1)+abs($x2)] [expr abs($y1)+abs($y2)] [expr abs($z1)+abs($z2)]] -all -molid top
 ##****Change below according to salt concentration (4places)**#
 $sel1 writepdb ${filex}_solvated.pdb 
 $sel1 writepsf ${filex}_solvated.psf
 mol delete all
 ## Display of box vector parameters ##
 mol new ${filex}_solvated.psf
 mol addfile ${filex}_solvated.pdb
 set sel2 [atomselect top all]
 set minmax [measure minmax $sel2] 
 set vec [vecsub [lindex $minmax 1] [lindex $minmax 0]] 
 puts "cellBasisVector1 $xsize 0 0" 
 puts "cellBasisVector2 0 $ysize 0" 
 puts "cellBasisVector3 0 0 $zsize" 
 set center [measure center $sel2] 
 puts "cellOrigin 0 0 0 "
 puts " Total Charge on System: [eval vecadd [$sel2 get charge]]"
 ##### The below part is written to copy the box vectors in the box_size.txt file ######
 set x [lindex $vec 0]
 set y [lindex $vec 1]
 set z [lindex $vec 2]
 set xcenter [lindex $center 0] 
 set ycenter [lindex $center 1]
 set zcenter [lindex $center 2]
 puts $outfile [format "cellBasisVector1 %2.2f 0 0 "  $xsize ]
 puts $outfile [format "cellBasisVector2 0 %2.2f 0 "  $ysize ]
 puts $outfile [format "cellBasisVector3 0 0 %2.2f "  $zsize ]
 ## deleting unnecessary files ##
 file delete with_water.pdb
 file delete with_water.psf
 file delete with_water.log
 file delete ionize.pdb
 file delete ionize.psf
 file delete half_water.psf
 file delete half_water.pdb
 file delete half_water.log
 close $outfile
 pbc box -color orange -style tubes -width 1 -center bb
 mol delete all
 resetpsf
 }
 exit
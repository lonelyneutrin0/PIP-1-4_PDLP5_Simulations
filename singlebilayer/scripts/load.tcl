set dcd_files [glob -nocomplain *.dcd]

set sorted [lsort $dcd_files]

foreach file $sorted { 
	mol addfile $file waitfor -1
}

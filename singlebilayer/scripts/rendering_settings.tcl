# Load files
mol new system.psf type psf waitfor all
mol addfile system.pdb type pdb waitfor all

# Wait until VMD GUI is ready
set molID [molinfo top]
update

# Set display settings
display rendermode {Tachyon RTX RTRT}
display ambientocclusion on
display shadows on
display background white
display projection orthographic
axes location off

mol delrep 0 $molID

# --- Membranes: VDW + AOChalky ---
mol selection {segname MEMB} 
mol representation VDW
mol color ColorID 6
mol addrep $molID
set repIndex [expr {[molinfo $molID get numreps] - 1}]
mol modmaterial $repIndex $molID AOChalky

# --- Protein: NewCartoon ---
mol selection {segname PROA PROB PROC PROD}
mol representation NewCartoon
mol color ColorID 3
mol addrep $molID

mol selection {segname PROE PROF PROG PROH}
mol representation NewCartoon
mol color ColorID 19
mol addrep $molID


# --- Water: QuickSurf + Transparent ---
mol selection {water}
mol representation QuickSurf
mol color ColorID 8
mol addrep $molID
set repIndex1 [expr {[molinfo $molID get numreps] - 1}]
mol modmaterial $repIndex1 $molID Transparent

# --- Ions: VDW
mol selection {ions}
mol representation VDW
mol color Name
mol addrep $molID 
set repIndex2 [expr {[molinfo $molID get numreps] - 1}]
mol modmaterial $repIndex2 $molID AOChalky


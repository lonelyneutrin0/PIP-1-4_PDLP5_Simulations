from vmd import atomsel, Molecule, evaltcl
from vmd import vmdnumpy as vnp

import glob
import numpy as np

from numpy.typing import NDArray

def loadtraj(psf_dir: str, dcd_dir: str = ".") -> Molecule:
	""" 
	Utility function to load psf and trajectory files

	Params:

	dcd_dir: (str)
		The directory in which the trajectory files are located (relative)

	psf_dir: (str)
		The directory in which the psf file is located (relative)

	Returns: 
		A loaded VMD molecule
	"""

	# Load the psf file
	mol = Molecule.Molecule()
	mol.load("%s/system.psf" % psf_dir)

	# Sort the trajectories in order
	dcdlist = sorted(glob.glob("%s/run*dcd" % dcd_dir))
	print(dcdlist)

	# Load the trajectories
	for dcd in dcdlist:
		#5000 2fs steps between dcd frames normally. So step 10 = 100ps per frame.
		mol.load(dcd, step=10)
	return mol

def recenter(mol):
	""" 
	Utility function to handle rewrapping and centering

	Params:

	mol: (Molecule)
		Given VMD Molecule to be centered
	"""

	# Unwrap the aquaporin tetramer
	evaltcl('''set mid %d
set asel [atomselect $mid "all"]
set psel [atomselect $mid "segname PROE PROF PROG PROH"]
fastpbc unwrap $psel
fastpbc wrap $asel centersel $psel compound fragment
''' % int(mol))

	# Center the membrane
	asel = atomsel("all", molid=int(mol))
	msel = atomsel("segname MEMB \"GLP.*\"", molid=int(mol))
	for f in range(mol.numFrames()):
		asel.frame = f
		msel.frame = f
		asel.moveby(-1 * np.array(msel.center()))

def watertracking(mol) -> NDArray:
	""" 
	Track the Z coordinates of water molecules throughout a trajectory

	Params: 

	mol: (Molecule)
		Given VMD Molecule

	Returns:
		NDArray (frames, num_waters) containing the Z coordinates of water molecules
	""" 

	# Get the indices of the water molecules
	watsel = atomsel("water and noh", molid=int(mol))
	watidx = np.array(watsel.index)

	# Add the water molecule Z coordinates to an NDArray
	watZ = np.empty((mol.numFrames(), len(watidx)), dtype=float)
	for f in range(mol.numFrames()):
		R = vnp.timestep(int(mol), f)
		watZ[f] = R[watidx,2]
	return watZ

PSF_DIR = "../../../../../builds/porinalone/grad/0.010/"

mol = loadtraj(PSF_DIR)
recenter(mol)
watz = watertracking(mol)
np.save("watz.npy", watz)
mol.delete()
exit()
from vmd import atomsel, Molecule, evaltcl
from vmd import vmdnumpy as vnp
import glob
import numpy as np
def loadtraj(d):
	mol = Molecule.Molecule()
	mol.load("%s/system.psf" % d)
	dcdlist = sorted(glob.glob("%s/run*dcd" % d))
	print(dcdlist)
	for dcd in dcdlist:
		#5000 2fs steps between dcd frames normally. So step 10 = 100ps per frame.
		mol.load(dcd, step=10)
	return mol
def recenter(mol):
	evaltcl('''set mid %d
set asel [atomselect $mid "all"]
set psel [atomselect $mid "segname PROE PROF PROG PROH"]
fastpbc unwrap $psel
fastpbc wrap $asel centersel $psel compound fragment
''' % int(mol))
	asel = atomsel("all", molid=int(mol))
	msel = atomsel("segname MEMB \"GLP.*\"", molid=int(mol))
	for f in range(mol.numFrames()):
		asel.frame = f
		msel.frame = f
		asel.moveby(-1 * np.array(msel.center()))

def watertracking(mol):
	watsel = atomsel("water and noh", molid=int(mol))
	watidx = np.array(watsel.index)
	watZ = np.empty((mol.numFrames(), len(watidx)), dtype=float)
	for f in range(mol.numFrames()):
		R = vnp.timestep(int(mol), f)
		watZ[f] = R[watidx,2]
	return watZ

for d in ['porinalone', 'porinwithcap']:
	for i in range(3):
		mol = loadtraj("../%s/%d" % (d,i))
		recenter(mol)
		watz = watertracking(mol)
		np.save("waterdata/%s_%d.npy" % (d, i), watz)
		mol.delete()
exit()
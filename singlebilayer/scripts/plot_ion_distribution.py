import numpy as np 
import matplotlib.pyplot as plt 
import matplotlib

# Get data from .dat files and initialize NumPy arrays
anions = np.loadtxt("anion_z.dat", dtype=float)[:, 1:]  # Exclude the first column, which is frame number
cations = np.loadtxt("cation_z.dat", dtype=float)[:, 1:]

print(anions.shape)
print(cations.shape)

# Parameters
Z_MAX = 85 
Z_MIN = -85 

BIN_SIZE = 5
NUM_FRAMES = anions.shape[0]

Discard the first half of the data 
anions = anions[NUM_FRAMES//2:, :]
cations = cations[NUM_FRAMES//2:, :]
NUM_FRAMES = NUM_FRAMES//2

# Create the bin and digitize the given data 
bins = np.arange(start=Z_MIN, stop=Z_MAX, step=BIN_SIZE)

cation_digitized = np.clip(np.digitize(cations, bins) - 1, 0, bins.size-1)
anion_digitized = np.clip(np.digitize(anions, bins) - 1, 0, bins.size-1)

# Count the occurrences of each bin
cation_bincount = np.zeros((NUM_FRAMES, bins.size))
anion_bincount = np.zeros((NUM_FRAMES, bins.size))



for idx, row in enumerate(cation_digitized):
    cation_bincount[idx] = np.bincount(row, minlength=bins.size)

for idx, row in enumerate(anion_digitized):
    anion_bincount[idx] = np.bincount(row, minlength=bins.size)

cation_hist = np.sum(cation_bincount, axis=0)/np.sum(cation_bincount, axis=(0, 1))
plt.hist(bins, weights=cation_hist)
plt.xlabel("z")
plt.ylabel("p(z)")
plt.title("Cation Distribution")
plt.show()

anion_hist = np.sum(anion_bincount, axis=0)/np.sum(anion_bincount, axis=(0, 1))
plt.hist(bins, weights=anion_hist)
plt.xlabel("z")
plt.ylabel("p(z)")
plt.title("Anion Distribution")
plt.show()

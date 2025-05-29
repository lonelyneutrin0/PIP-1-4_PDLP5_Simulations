from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from io import StringIO

epot = StringIO()

# --- Step 1: Constants
with open('epot.dx', 'r') as f: 
	lines = f.readlines()

	gridpoint_line = lines[1].split(' ')
	cx, cy, cz = int(gridpoint_line[5]), int(gridpoint_line[6]), int(gridpoint_line[7])

	origin_line = lines[2].split(' ')
	oz = float(origin_line[3])

	delta_line = lines[5].split(' ')
	dz = float(delta_line[3])

	trimmed_lines = lines[8:-5]
	for line in trimmed_lines:
		epot.write(line + '\n')

epot.seek(0)

# --- Step 2: Extract first 3 columns from `epot.dx` into vv.dat, one value per line
with epot as infile, open('vv.dat', 'w') as outfile:
    for line in infile:
        values = line.strip().split()
        for val in values[:3]:  # print $1, $2, $3 in separate lines
            outfile.write(val + '\n')

# --- Step 3: Generate vz.dat (like seq in shell)
fz = oz + cz * dz
vz = np.arange(oz, fz + dz/2, dz)  # Add small buffer to include last value due to float precision
np.savetxt('vz.dat', vz, fmt='%.6f')

# --- Step 4: Compute v0 and vf (line indices)
v0 = int(cz * cy * cx / 2 + cz * cy / 2)
vf = v0 + cz

print("v0:", v0)
print("vf:", vf)

# --- Step 5: Extract lines from vv.dat (line indices v0 to vf-1) into vv2.dat
with open('vv.dat', 'r') as infile:
    lines = infile.readlines()

with open('vv2.dat', 'w') as outfile:
    outfile.writelines(lines[v0:vf])

# --- Step 6: Combine vz.dat and vv2.dat into zpotential.dat
vz_data = np.loadtxt('vz.dat')
vv2_data = np.loadtxt('vv2.dat')

# Ensure both arrays are the same length before stacking
min_length = min(len(vz_data), len(vv2_data))
vz_data = vz_data[:min_length]
vv2_data = vv2_data[:min_length]

# Now stack them
combined = np.column_stack((vz_data, 0.0258 * vv2_data))
np.savetxt('zpotential.dat', combined, fmt='%.6f')
plt.plot(vz_data, 0.0258* vv2_data)
plt.title(input())
plt.xlabel('z')
plt.ylabel('Potential [V]')
plt.savefig("plot.png")
plt.show()






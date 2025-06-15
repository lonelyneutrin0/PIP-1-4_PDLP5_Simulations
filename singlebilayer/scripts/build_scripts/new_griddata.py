import numpy as np

# Grid shape to match the working one
shape = (2, 2, 144)
data = np.zeros(shape).reshape(-1, 3)

# Origin and spacing from your valid PME file
origin = np.array([-76.172, -77.492, -72.226]) # ADD THE ORIGIN OF THE PERIODIC CELL HERE
delta = np.array([10.0, 10.0, 1.0])

header_str = f"""object 1 class gridpositions counts {shape[0]} {shape[1]} {shape[2]}
origin {origin[0]} {origin[1]} {origin[2]}
delta {delta[0]} 0 0
delta 0 {delta[1]} 0
delta 0 0 {delta[2]}
object 2 class gridconnections counts {shape[0]} {shape[1]} {shape[2]}
object 3 class array type double rank 0 items {data.size} data follows\n"""

with open('potential.dx', 'w', encoding='utf-8') as f: 
    f.write(header_str)

with open('potential.dx', 'a', encoding='utf-8') as f: 
    np.savetxt(fname=f, X=data, fmt='%.4f')
    f.write("""attribute "dep" string "positions"
object "PME potential (kT/e, T=300K)" class field
component "positions" value 1
component "connections" value 2
component "data" value 3
""")
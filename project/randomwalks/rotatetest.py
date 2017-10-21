import numpy as np
N = 3
for i in range(N+1):
    for j in range(N+1):
        pos = [i,j]
        pos = [2*val-N for val in pos]
        #print(pos)
        rotated = [pos[0]/np.sqrt(2)+pos[1]/np.sqrt(2), -pos[0]/np.sqrt(2)+pos[1]/np.sqrt(2)]
        rotated = [i*np.sqrt(2)/2 for i in rotated]
        #print(str(pos) + ' '+str(rotated)+'  '+str(sum(rotated)))
        print( ' '+str(rotated)+'  '+str(abs(rotated[0]) + abs(rotated[1])))

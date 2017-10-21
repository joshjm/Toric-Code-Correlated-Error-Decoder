import walks
import numpy as np
import sys
import time
file = open('manhat_pythag_data.txt','w')

pythag_data =[]
manhat_data =[]
N = 32
L = 2*N + 1
array = np.zeros((2*L,2*L))
outerrange = 1000
for i in range(outerrange):
    for j in range(1000):
        #generate walk
        returned = walks.type4(array,L,N)
        displacement = [returned[0], returned[1]]
        endpoint = [returned[2], returned[3]]
        file.write(str(abs(displacement[0])+abs(displacement[1]))+', '+str(np.sqrt(pow(displacement[0],2)+pow(displacement[1],2)))+'\n')
    sys.stdout.write("\r" +'percent done: '+ str(100.0*i/outerranger)+'  '+time.ctime())
    sys.stdout.flush()
print('\n complete \n')

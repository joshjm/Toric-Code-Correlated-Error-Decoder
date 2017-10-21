import funmath
funmath.tic()
import walks
import math
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import seaborn as sns
import random
import exactwalklengthcalculator as ex
file = open('manhat_pythag_data.txt','w')

pythag_data =[]
manhat_data =[]
N = 32
L = 2*N + 1
array = np.zeros((2*L,2*L))
loops = 1000
for i in range(loops):
    #generate walk
    returned = walks.type4(array,L,N)
    displacement = [returned[0], returned[1]]
    endpoint = [returned[2], returned[3]]

    #get manhatten distance of endpoint
    manhat_data.append(abs(displacement[0])+abs(displacement[1]))
    #get Pythagorean distance of endpoint
    pythag_data.append(np.sqrt(pow(displacement[0],2)+pow(displacement[1],2)))

    file.write(str(manhat_data[-1])+', '+str(pythag_data[-1])+'\n')

#plot distributions
sns.set_style('whitegrid')

bandwidth = 1
sns.kdeplot(np.array(pythag_data), bw=bandwidth, color = 'b', label = "Pythagorean Density plot")
sns.kdeplot(np.array(manhat_data), bw=bandwidth, color = 'r', label = "Manhattan Density plot")

sns.rugplot(pythag_data, color='r')
plt.scatter([], [], marker="|", color='r',linewidth=2, s=100, label="pythag_data rugplot")


sns.rugplot(manhat_data, color='b')
plt.scatter([], [], marker="|", color='b',linewidth=2, s=100, label="manhat_data rugplot")
#plot expected walk length line
pythag_expected = ex.walklengthcalc(N)[0]
manhat_expected = ex.walklengthcalc(N)[1]
plt.plot([pythag_expected]*10,np.linspace(0,1,10),  'b--', label = "expected pythag walk length")
plt.plot([manhat_expected]*10,np.linspace(0,1,10),  'r--', label = "expected manhat walk length")
plt.plot([np.sqrt(N)]*10,np.linspace(0,1,10),  'k--', label = "$\sqrt{N}$")

plt.legend()
plt.xlabel('Walk length')
plt.ylabel('Density')
plt.suptitle('Distribution of walk lengths')
plt.title('steps (N) = '+str(N)+', '+str(loops)+' simulated walks, Bandwidth = '+str(bandwidth))
plt.savefig('figs/'+'randomwalkdistribution_'+str(loops)+'_'+str(N)+'.pdf')
funmath.toc()

plt.show()

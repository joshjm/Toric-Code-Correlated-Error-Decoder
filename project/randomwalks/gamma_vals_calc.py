import funmath
import walks
import math
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import random
from scipy.stats import gamma
from scipy.stats import kstest
import exactwalklengthcalculator as ex
funmath.tic()
file = open('gamma_info.txt','w')

loops = 1000000
N=32
rawdata = np.loadtxt('manhat_pythag_data.txt' ,  delimiter=',', skiprows=0, unpack=False)

manhat_data = rawdata[:,0]
pythag_data = rawdata[:,1]

#fit a gamma distribution
    #to the pythag data
pythag_fit_alpha, pythag_fit_loc, pythag_fit_beta = gamma.fit(pythag_data)
pythag_dist = gamma(pythag_fit_alpha, pythag_fit_loc, pythag_fit_beta )

    #to the manhat data
manhat_fit_alpha, manhat_fit_loc, manhat_fit_beta = gamma.fit(manhat_data)
manhat_dist = gamma(manhat_fit_alpha, manhat_fit_loc, manhat_fit_beta )


#save info

file.write(str(pythag_fit_alpha)+','+ str(pythag_fit_loc)+',' + str(pythag_fit_beta)+'\n')
file.write(str(manhat_fit_alpha)+','+ str(manhat_fit_loc)+',' + str(manhat_fit_beta)+'\n')
file.close()
funmath.toc()
x = [i*max(manhat_data)/100.0 for i in range(0,100,1)]
    #plot  pythag distribution


#print locations of max vals
loc1 = x[np.argmax(pythag_dist.pdf(x))]
loc2 = x[np.argmax(manhat_dist.pdf(x))]

print('mac loc'+str([loc1, loc2]))
print('max vals '+str([(pythag_dist.pdf(loc1)), (manhat_dist.pdf(loc2)) ]))

plt.plot(x, pythag_dist.pdf(x), color = 'b', label = "Pythagorean Density plot")
    #plot manhat distribution
plt.plot(x, manhat_dist.pdf(x), color = 'r', label = "Manhattan Density plot")
x = range(0,33,2)
print([manhat_dist.pdf(i) for i in x ])

#plot expected walk length line
ymax = 0.2
pythag_expected = ex.walklengthcalc(N)[0]
manhat_expected = ex.walklengthcalc(N)[1]
plt.plot([pythag_expected]*10,np.linspace(0,ymax,10),  'b--', label = "expected pythag walk length")
plt.plot([manhat_expected]*10,np.linspace(0,ymax,10),  'r--', label = "expected manhat walk length")
plt.plot([np.sqrt(N)]*10,np.linspace(0,ymax,10),  'k--', label = "$\sqrt{N}$")
plt.axis([0, max(manhat_data), 0, ymax])
plt.legend()
plt.xlabel('Walk length (N)')
plt.ylabel('Density')
plt.suptitle('Distribution of walk lengths')
plt.title('steps (N) = '+str(N)+', '+str(loops)+' simulated walks : fitted gamma functions')
plt.savefig('figs/'+'randomwalkdistribution_'+str(loops)+'_'+str(N)+'.pdf')

plt.show()

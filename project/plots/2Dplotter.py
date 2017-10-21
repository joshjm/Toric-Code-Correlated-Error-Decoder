
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure()
#ax.plot(pnuc, l, zs=0.5, zdir='z', label='CorrLen = L$\sqrt{P_{Nuc}}$')

filename = 'l1000000L40True_9d6be54c85d543199f996f4a5482f531'
rawdata = np.loadtxt('data/'+filename+'.txt' ,  delimiter=',', skiprows=1, unpack=False)
#check for non-zero starting point
i=0

q1fail = rawdata[:,4]
q2fail = rawdata[:,5]
qfail = [(q1fail[i]+q2fail[i])/2 for i in range(len(q1fail))]
numsamples = 1000000

expectedlength = rawdata[:,3]


plt.plot(expectedlength, q1fail,'r.',label = 'Code failure rate')
#plt.plot([0,20], [0.1987,0.1987],'b-',label = 'Unadjusted failure rate')
#plt.plot([5.016,5.016], [0,0.5],'k--',label = 'Expected walk length')
linestyle = {"linestyle":"", "linewidth":1, "markeredgewidth":1, "elinewidth":1, "capsize":2} #define error bars
yerror = [1.96*np.sqrt((1.0/numsamples)*i*(1.0-i)) for i in q1fail]
plt.errorbar(expectedlength, q1fail, yerr = yerror, color = 'k', **linestyle)
plt.xlabel('Expected walk length ($\overline{x}$)')
plt.ylabel('Failure Rate ($p$)')
plt.legend(loc=4)
#plt.axis([3.8, 6, 0.197 , 0.21])


#txt = '''colour shows levels of equal number of total errors ($P_{Nuc}\cdot $Corr Len)'''
#fig.text(.15,.05,txt)
plt.suptitle('Comparison of expected length calculations with gaussian correction')
plt.title('L = 40, N = 32, Anyons = 15, $\sigma^2$ = 10.75')
plt.grid(True)
plt.savefig('figs/'+'comparison_of_methods'+'.pdf')

plt.show()

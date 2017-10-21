
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def bi_err(val, n):
    return(1.96*np.sqrt((1.0/n)*val*(1.0-val)))

fig = plt.figure()
#ax.plot(pnuc, l, zs=0.5, zdir='z', label='CorrLen = L$\sqrt{P_{Nuc}}$')

filename = '4to8'
rawdata = np.loadtxt('data/'+filename+'.txt' ,  delimiter=',', skiprows=1, unpack=False)
#check for non-zero starting point
i=0

q1fail = rawdata[:,4]
q2fail = rawdata[:,5]
qfail = [(q1fail[i]+q2fail[i])/2 for i in range(len(q1fail))]
n = 60000

variance = rawdata[:,0]
xmin = variance[0]
xmax = variance[-1]
ymin = 0.1
ymax = 0.3

hline = 0.202745833333333
hline_err = bi_err(hline,200000)

plt.plot(variance, q1fail,'r-',label = 'q1 failure rate')
plt.plot(variance, q2fail,'b-',label = 'q2 failure rate')
plt.plot([xmin,xmax], [hline,hline],'g-',label = 'Unadjusted failure rate: '+str(round(10000*hline)/10000)+'$\pm$'+str(round(10000*hline_err)/10000))
#error bars
linestyle = {"linestyle":"", "linewidth":1, "markeredgewidth":1, "elinewidth":1, "capsize":2} #define error bars
y1error = [bi_err(val,n) for val in q1fail]
y2error = [bi_err(val,n) for val in q2fail]
plt.errorbar(variance, q1fail, yerr = y1error, color = 'k', **linestyle)
plt.errorbar(variance, q2fail, yerr = y2error, color = 'k', **linestyle)

plt.xlabel('Variance of correction function ($\sigma^2$) ')
plt.ylabel('Failure Rate ($p$)')
plt.legend(loc=4)
plt.axis([xmin, xmax, ymin,  ymax])


#txt = '''colour shows levels of equal number of total errors ($P_{Nuc}\cdot $Corr Len)'''
#fig.text(.15,.05,txt)
plt.suptitle('Varying Variance')
plt.title('Code size = 40, Walk length = 32, Real expected = 5.016, loops = '+str(n))
plt.grid(True)
plt.savefig('figs/'+'improvement'+str(filename)+'.pdf')

plt.show()

"""plots the failurerate vs strength"""
from mpl_toolkits.mplot3d import Axes3D
import collections
import operator
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
import matplotlib.mlab as ml
""" this function will make heat plots of [var, expected, qfail] data in any
    combination. Will create seperate plots of each different value for the
    number of anyons.
"""
#filename = 'highMT_l_18000_13b760e3433c4560933c1216cd6774dc'
#filename = 'highMT_l_40000_cb85a9498bae460cbdb61a1a8df1a462'
#filename = 'highMT_l_18000_13b760e3433c4560933c1216cd6774dc'
#filename = 'highMT_l_90000_707eff2243e145af94fd273e0388f1cd'
filename = 'highMT_l_10000_e835ffc589de422ca2f195f7c6b1e027'
dat = np.loadtxt('data/'+filename+'.txt' ,  delimiter=',', skiprows=1, \
                  usecols = (2,4,7), unpack=False)

numsamples = 10000 # 2 qubits averaged?

# Load data from CSV

strength = dat[:,0]
anyons = dat[:,1]
qfail = dat[:,2]

datadict = collections.defaultdict(list)

for i in range(len(strength)): # group data by number of anyons
    datadict[anyons[i]].append([strength[i],qfail[i]])

for key in datadict:
    # get data for this anyon number
    strength = [val[0] for val in datadict[key]]
    qfail = [val[1] for val in datadict[key]]
    #sort it into order
    L = sorted(zip(strength,qfail), key=operator.itemgetter(0))
    strength, qfail = zip(*L)
    plt.plot(strength, qfail, '*-', label = str(key))
    # error bars
    yerror = [1.96*np.sqrt((1.0/numsamples)*i*(1.0-i)) for i in qfail]
    linestyle = {"linestyle":"", "linewidth":1, "markeredgewidth":1, "elinewidth":1, "capsize":2} #define error bars
    plt.errorbar(strength, qfail, yerr = yerror, color = 'k', **linestyle)
    # plt
    plt.legend()
    plt.ylabel('Failure rate')
    plt.xlabel('strength ($\sigma^2$)')
    plt.suptitle('Strength Vs Failure Rate')
    plt.title('Exact Manhattan PDF correction method')
    plt.savefig('figs/exactpdfstrength_A'+str(key)+'_'+filename+'.pdf')

plt.show()
plt.close()

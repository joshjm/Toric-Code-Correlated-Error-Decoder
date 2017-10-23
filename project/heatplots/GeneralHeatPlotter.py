from mpl_toolkits.mplot3d import Axes3D
import collections

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
filename = 'highMT_l_10000_6c72e34cdfba4c059f36140c5d351e59'
dat = np.loadtxt('data/'+filename+'.txt' ,  delimiter=',', skiprows=1, \
                  usecols = (1,3,4,7), unpack=False)

numsamples = 40000

# Load data from CSV

expected = dat[:,0]
variance = dat[:,1]
anyons = dat[:,2]
qfail = dat[:,3]


datadict = collections.defaultdict(list)

for i in range(len(expected)): # group data by number of anyons
    datadict[anyons[i]].append([expected[i],variance[i],qfail[i]])

for key in datadict:

    expected = [val[0] for val in datadict[key]]
    variance = [val[1] for val in datadict[key]]
    qfail = [val[2] for val in datadict[key]]

    x = np.unique(expected) # list of all expected values tested
    y = np.unique(variance) # list  of all varince values tested
    print(x)
    print(y)
    X,Y = np.meshgrid(x,y)
    z = np.array(qfail)
    Z = z.reshape(len(y),len(x))
    Z = griddata((expected, variance), qfail, (X,Y), method='linear')
    #plt.plot(expected, variance, qfail)


    #plt.pcolormesh(X,Y,Z, shading ='gouraud')
    plt.pcolormesh(X,Y,Z,cmap = plt.get_cmap('rainbow'))
    plt.colorbar()


    plt.xlabel('expected distance ($\overline{w}$)')
    plt.ylabel('variance ($\sigma^2$)')
    plt.suptitle('Variance Vs Gaussian location')
    plt.title('L = 40, N = 32, A = '+str(key))
    plt.savefig('figs/2dplot_A'+str(key)+'_'+filename+'.pdf')

    plt.show()
    plt.close()

from mpl_toolkits.mplot3d import Axes3D

import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
import matplotlib.mlab as ml
filename = 'highMT_l_18000_13b760e3433c4560933c1216cd6774dc'
dat = np.loadtxt('data/'+filename+'.txt' ,  delimiter=',', skiprows=1, \
                  usecols = (1,3,4,7), unpack=False)

numsamples = 10000

# Load data from CSV

expected = dat[:,0]
variance = dat[:,1]
anyons = dat[:,2]
qfail = dat[:,3]

datadict = {}
datadict[8] = []
datadict[12] = []
datadict[16] = []
for i in range(len(expected)):
    datadict[anyons[i]].append([expected[i],variance[i],qfail[i]])
for i in [8,12,16]:

    xmin = 4 #expected
    xmax = 7
    nx = 15 #numer of steps
    ymin = 1 #variance
    ymax = 15
    ny = 15

    expected = [val[0] for val in datadict[i]]
    variance = [val[1] for val in datadict[i]]
    qfail = [val[2] for val in datadict[i]]

    x=np.unique(expected)
    y=np.unique(variance)
    X,Y = np.meshgrid(x,y)
    z = np.array(qfail)
    Z=z.reshape(len(y),len(x))
    #plt.plot(expected, variance, qfail)


    plt.pcolormesh(X,Y,Z, shading ='gouraud')
    #plt.pcolormesh(X,Y,Z,cmap = plt.get_cmap('rainbow'))
    plt.colorbar()


    plt.xlabel('expected distance ($\overline{w}$)')
    plt.ylabel('variance ($\sigma^2$)')
    plt.suptitle('Variance Vs Gaussian location')
    plt.title('L = 40, N = 32')
    plt.savefig('figs/2dplot__'+filename+'.pdf')

    plt.show()
    plt.close()

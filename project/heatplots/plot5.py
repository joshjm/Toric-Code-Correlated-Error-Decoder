import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
import matplotlib.mlab as ml
filename = 'highMT_l_10000_6ae1878c5758453ab7400f00f7bc7882'
dat = np.loadtxt('data/'+filename+'.txt' ,  delimiter=',', skiprows=1, usecols = (1,3,7), unpack=False)

qfail = dat[:,2]
numsamples = 10000

# Load data from CSV

x = dat[:,0]
y = dat[:,1]
z = qfail
xmin = 0 #expected
xmax = 7
nx = 30 #numer of steps
ymin = 1 #variance
ymax = 20
ny = 30
xi = np.linspace(xmin, xmax, nx)
yi = np.linspace(ymin, ymax, ny)
zi = ml.griddata(x, y, z, xi, yi, 'linear')
plt.xlabel('expected distance ($\overline{w}$)')
plt.ylabel('variacne ($\sigma^2$)')
#CS = plt.contour(xi, yi, zi, 15, linewidths=0.5, colors='k')
CS = plt.pcolormesh(xi, yi, zi, cmap = plt.get_cmap('rainbow'))
plt.colorbar(CS, orientation='vertical', shrink=0.8)
plt.suptitle('Variance Vs Gaussian location')
plt.title('L = 40, N = 32, Anyons = 15')
#plt.grid(True)
#plt.colorbar()
plt.savefig('figs/'+'variancevslocation_'+filename+'.pdf')
plt.savefig('figs/'+'variancevslocation_'+filename+'.png')
plt.show()

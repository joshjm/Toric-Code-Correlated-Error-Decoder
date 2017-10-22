import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
import matplotlib.mlab as ml
filename = 'highMT_l_10000_6c72e34cdfba4c059f36140c5d351e59'
dat = np.loadtxt('data/'+filename+'.txt' ,  delimiter=',', skiprows=1, usecols = (1,3,7), unpack=False)

qfail = dat[:,2]
numsamples = 10000

# Load data from CSV

x = dat[:,0]
y = dat[:,1]
z = qfail
print(sum(qfail)/len(qfail))
print(len(qfail))
xmin = 0 #expected
xmax = 8
nx = 40 #numer of steps
ymin = 1 #variance
ymax = 41
ny = 40
xi = np.linspace(xmin, xmax, nx)
yi = np.linspace(ymin, ymax, ny)
zi = ml.griddata(x, y, z, xi, yi, 'linear')
plt.xlabel('expected distance ($\overline{w}$)')
plt.ylabel('variance ($\sigma^2$)')
#CS = plt.contour(xi, yi, zi, 15, linewidths=0.5, colors='k')
CS = plt.pcolormesh(xi, yi, zi, cmap = plt.get_cmap('rainbow'))
plt.colorbar(CS, orientation='vertical', shrink=0.8, label = 'Failure rate')
plt.suptitle('Variance Vs Gaussian location')
plt.title('L = 40, N = 32, Anyons = 4')
#plt.grid(True)
#plt.colorbar()
plt.savefig('figs/'+'variancevslocation_'+filename+'.pdf')
plt.savefig('figs/'+'variancevslocation_'+filename+'.png')
plt.show()

import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
import matplotlib.mlab as ml
filename = 'highMT_l_3400_ac7e166d364445f7bc9d746582ee3392'
dat = np.loadtxt('data/'+filename+'.txt' ,  delimiter=',', skiprows=1, unpack=False)

qfail = dat[:,6]
numsamples = 10000

# Load data from CSV

x = dat[:,1]
y = dat[:,3]
z = qfail
xmin = 0
xmax = 10
nx = 20 #numer of steps
ymin = 0
ymax = 20
ny = 20
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

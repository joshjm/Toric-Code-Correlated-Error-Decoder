import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
import matplotlib.mlab as ml
filename = 'highMT_l_50000_93a5d5e5843c4d849a430a5a3885eb24'
dat = np.loadtxt('data/'+filename+'.txt' ,  delimiter=',', skiprows=1, unpack=False)

qfail = dat[:,6]
numsamples = 50000

# Load data from CSV

x = dat[:,1] #expected val
y = dat[:,3] #variance
z = qfail
xmin = min(x)
xmax = max(x)
print([xmin,xmax])
xss = 0.2 #step size
nx = (xmax - xmin )/xss#10  #number of steps
print(nx)
ymin = min(y)
ymax = max(y)
print([ymin,ymax])
yss = 0.25 #step size
ny = (ymax - ymin )/yss #10  #number of steps
print('min failure: '+str(min(z)))
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

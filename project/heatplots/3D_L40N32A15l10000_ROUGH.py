from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
import pandas as pd
from sys import argv

filename = 'highMT_l_3400_ac7e166d364445f7bc9d746582ee3392'
dat = np.loadtxt('data/'+filename+'.txt' ,  delimiter=',', skiprows=1, unpack=False)

n = 3400 #numsamples

# Load data from CSV
fig = plt.figure()
ax = fig.gca(projection='3d')
x = dat[:,1]
y = dat[:,3]
z = dat[:,6]

#calc error
p = 0.2  #value to calculate error for
sigma = 1.96 #confidence interval
zerror = [1.0*sigma*np.sqrt((1.0/n)*p*(1.0-p)) for p in z]
xmin = 0
xmax = 8
nx = 12 #numer of steps
ymin = 0
ymax = 21
ny = 10

df = pd.DataFrame({'x': x, 'y': y, 'z': z})
fig = plt.figure()
ax = Axes3D(fig)
surf = ax.plot_trisurf(df.x, df.y, df.z, cmap=cm.jet, linewidth=0.1)
fig.colorbar(surf, shrink=0.5, aspect=5)

#draw errorbars
for i in range(len(x)):
    ax.plot([x[i], x[i]], [y[i], y[i]], [z[i]+zerror[i], z[i]-zerror[i]], 'k',marker="_")

plt.xlabel('expected distance ($\overline{w}$)')
plt.ylabel('variacne ($\sigma^2$)')
#CS = plt.contour(xi, yi, zi, 15, linewidths=0.5, colors='k')
# Plot the surface.
#ax.scatter(x, y, z)#plt.colorbar(CS, orientation='vertical', shrink=0.8)

plt.suptitle('Variance Vs Gaussian location')
plt.title('L = 40, N = 32, Anyons = 15')
#plt.grid(True)
#plt.colorbar()
plt.savefig('figs/'+'surface_'+filename+'.pdf')
plt.savefig('figs/'+'surface'+filename+'.png')
plt.show()

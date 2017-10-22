
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
import matplotlib.mlab as ml
filename = 'highMT_l_40000_cb85a9498bae460cbdb61a1a8df1a462'
dat = np.loadtxt('data/'+filename+'.txt' ,  delimiter=',', skiprows=1, \
                  usecols = (1,3,4,7), unpack=False)

numsamples = 10000

# Load data from CSV

expected = dat[:,0]
variance = dat[:,1]
anyons = dat[:,2]
qfail = dat[:,3]

datadict = {}
datadict[4] = {}
datadict[8] = []
datadict[12] = []
datadict[16] = []
for i in range(len(expected)):
    datadict[anyons[i]].append([expected[i],variance[i],qfail[i]])
for i in [4,8,12,16]:
    xmin = 4 #expected
    xmax = 7
    nx = 15 #numer of steps
    ymin = 1 #variance
    ymax = 15
    ny = 15

    expected = [val[0] for val in datadict[i]]
    variance = [val[1] for val in datadict[i]]
    qfail = [val[2] for val in datadict[i]]

    xi = np.linspace(xmin, xmax, nx)
    yi = np.linspace(ymin, ymax, ny)
    zi = ml.griddata(expected, variance, qfail, xi, yi, 'linear')
    plt.xlabel('expected distance ($\overline{w}$)')
    plt.ylabel('variance ($\sigma^2$)')
    #CS = plt.contour(xi, yi, zi, 15, linewidths=0.5, colors='k')
    CS = plt.pcolormesh(xi, yi, zi, cmap = plt.get_cmap('rainbow'))
    plt.colorbar(CS, orientation='vertical', shrink=0.8, label = 'Failure rate')
    plt.suptitle('Variance Vs Gaussian location')
    plt.title('L = 40, N = 32, Anyons = 4')
    #plt.grid(True)
    #plt.colorbar()
    plt.savefig('figs/'+'A'+str(i)+'__'+filename+'.pdf')

    plt.show()

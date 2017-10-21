
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import numpy as np
import os,sys,inspect
import imageio
from scipy.stats import gamma

rawdata = np.loadtxt('gamma_info.txt' ,  delimiter=',', skiprows=0, unpack=False)

sys.path.insert(1, os.path.join(sys.path[0], '..')) #go up a dir to import
import CodePy2.funmath as funmath
#import imageio
n = 100.0
N = int(np.sqrt(2*40*40)/2+1) #gives the maximum possible matching distance
sizes = [i/n  for i in range(N*int(n))]
xvals = sizes
#read information about the gamma functions
manhat_info = rawdata[1]
pythag_info = rawdata[0]
manhat_gamma = gamma(manhat_info[0], manhat_info[1], manhat_info[2])
pythag_gamma = gamma(pythag_info[0], pythag_info[1], pythag_info[2])
#generate y vals from gamma functions

manhat_yvals = [manhat_gamma.pdf(i) for i in xvals]
pythag_yvals = [pythag_gamma.pdf(i) for i in xvals]
index_max_pythag = np.argmax(pythag_yvals)
index_max_manhat = np.argmax(manhat_yvals)

print('max manhat: '+ str(xvals[index_max_manhat]))
print('max pythag: '+ str(xvals[index_max_pythag]))

inverted_manhat_yvals = [1-i/max(manhat_yvals) for i in manhat_yvals]
inverted_pythag_yvals = [1-i/max(pythag_yvals) for i in pythag_yvals]
filenames = []

scaled_manhat_yvals = [xvals[i]*inverted_manhat_yvals[i] for i in range(len(xvals))]
scaled_pythag_yvals = [xvals[i]*inverted_pythag_yvals[i] for i in range(len(xvals))]

plt.plot(xvals,scaled_manhat_yvals,'r-', label = 'Manhattan')
plt.plot(xvals,scaled_pythag_yvals,'b-',label = 'Pythagorean')

#plot gaussians too
gauss_manhat_yvals = [funmath.getnormval(i,6.358192239869876,1,10.75) for i in xvals]
gauss_pythag_yvals = [funmath.getnormval(i,5.016712342283284,1,10.75) for i in xvals]

plt.plot(xvals, gauss_manhat_yvals, 'r--', label = 'gaussian $\overline{x}$ = manahat $\sigma^2$=10.75')
plt.plot(xvals, gauss_pythag_yvals, 'b--', label = 'gaussian $\overline{x}$ = manahat $\sigma^2$=10.75')


plt.grid(True)
plt.ylabel('Adjusted weight (A)')
plt.xlabel('Manhatten distance (M)')
plt.axis([0, N, 0, N])
plt.legend()
plt.title('Gamma functions adjusted matching distances')
plt.suptitle('Reductions formed from walk distributions')
filename = 'gamma/'+'gamma_corrections'+'.pdf'
plt.savefig(filename)
filenames.append(filename)
#plt.close()
plt.show()
#os.system("avconv -y -f image2 -i figs/gaussian-%d.png -r 10 -s 800x600 gaussianvideo.avi")

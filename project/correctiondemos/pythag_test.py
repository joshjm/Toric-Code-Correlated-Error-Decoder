
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import numpy as np
import os,sys,inspect
import imageio

sys.path.insert(1, os.path.join(sys.path[0], '..')) #go up a dir to import
import CodePy2.funmath as funmath
#import imageio
n = 1.0
sizes = [i/n  for i in range(33*int(n))]

xvals = sizes
filenames = []
for expectedlength in sizes:
    yvals = []
    fig = plt.figure()
    for i in sizes:
        variance = 1
        strength = 1
        yvals.append(funmath.getnormval(i,expectedlength,strength,variance))
        maxval = mlab.normpdf(expectedlength, expectedlength, np.sqrt(variance))

        #yvals[-1] = yvals[-1]*strength/maxval

    plt.plot(xvals,yvals)
    plt.grid(True)
    plt.ylabel('Adjusted weight (A)')
    plt.xlabel('Manhatten distance (M)')
    plt.axis([0, 30, 0, 30])
    plt.title('Gaussian adjusted matching distances')
    plt.suptitle('variance = '+str(variance)+', w = '+str(expectedlength))
    filename = 'gaussian/'+'gaussian-'+str(int(expectedlength*n))+'.png'
    plt.savefig(filename)
    filenames.append(filename)
    plt.close()
    #plt.show()
#os.system("avconv -y -f image2 -i figs/gaussian-%d.png -r 10 -s 800x600 gaussianvideo.avi")

#turn into gif
images = []
for filename in filenames:
    images.append(imageio.imread(filename))
imageio.mimsave('xbar_demo.gif', images)

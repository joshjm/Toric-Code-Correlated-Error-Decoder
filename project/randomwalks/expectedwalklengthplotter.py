import funmath
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import numpy as np
import exactwalklengthcalculator as ex
fig = plt.figure()
#rawdata = np.loadtxt('expectedlengths.txt' ,  delimiter=',', skiprows=0, unpack=False)

#xvals = [i[0] for i in rawdata[:]]
#yvals = [i[1] for i in rawdata[:]]
xvals = range(32)
pythag_yvals = [ex.walklengthcalc(i)[0] for i in xvals]
manhat_yvals = [ex.walklengthcalc(i)[1] for i in xvals]
sqrt_yvals = [np.sqrt(i) for i in xvals]
plt.plot(xvals,pythag_yvals, 'r*-', label = 'Pythagorean distance')
plt.plot(xvals,manhat_yvals, 'b.-', label = 'Manhattan distance')
plt.plot(xvals,sqrt_yvals, 'g-', label = '$\sqrt{N}$')
plt.legend()
plt.xlabel('walk length ($N$)')
plt.ylabel('Distance weight ( $f(N)$ )')
plt.title('Expected displacement Vs Walk length')
plt.suptitle('Random walk in 2D')
plt.savefig('figs/'+'expectedwalklengths'+'.pdf')


plt.show()

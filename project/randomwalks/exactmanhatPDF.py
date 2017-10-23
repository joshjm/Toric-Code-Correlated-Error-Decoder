import math
import matplotlib.pyplot as plt
import funmath
import itertools
import collections
import numpy as np
from scipy.stats import gamma

def nCr(n,r):
    f = math.factorial
    return f(n) / f(r) / f(n-r)

def Prob(N,L):
    s = range( int((N-L)/2),      int((N+L)/2+1),  1) #range doesnt include end point
    p = range( int((N-L)/2+1),    int((N+L)/2),    1)
    #print([s,p])
    sum1 = 0
    for i in s:
        for j in s:
            sum1 += nCr(N,i)*nCr(N,j)
    sum2 = 0
    for i in p:
        for j in p:
            sum2 += nCr(N,i)*nCr(N,j)
    sum3 = 0
    for i in range(N+1):
        for j in range(N+1):
            sum3 += nCr(N,i)*nCr(N,j)
    return(1.0*(sum1-sum2)/sum3)

if __name__ == '__main__':
    #L = 4

    marker = itertools.cycle((',', '+', '.', 'o', '*'))
    funmath.tic()
    # N = 32
    #
    # rawdata = np.loadtxt('manhat_pythag_data.txt' ,  delimiter=',', skiprows=0, unpack=False)
    # manhat_data = rawdata[:,0]
    # datadict = collections.defaultdict(float)
    # for i in manhat_data:
    #     datadict[i] += 1
    # print(datadict)
    # yvals = []
    # for i in range(len(datadict)):
    #     dicval = datadict[2*i]/len(manhat_data)
    #     yvals.append(dicval)
    #     print(dicval)
    # xvals = range(0,len(yvals)*2,2)
    ###########################################################################
    #for N in [4,8,16,32,64]:
    for N in [32]:
        x = range(0,N+2,2)
        y = [Prob(N,L) for L in x]
        plt.plot(x,y, '.--', label  = 'Calculated Exact values')
        pdf_data = open('PDF_data_N'+str(N)+'.txt', 'w')
        
        for i in range(len(x)):
            pdf_data.write(str(x[i])+', ')
        pdf_data.write('\n')
        for i in range(len(x)):
            pdf_data.write(str(y[i])+', ')
        pdf_data.write('\n')

    ###########################################################################
    # plt.plot(xvals, yvals, '_', label  = 'Actual Walk Data' )
    # n = 1000*1000
    # z = 1.96
    # yerr = [1.0*z*np.sqrt((1.0/n)*p*(1.0-p)) for p in yvals]
    # #plt.errorbar(xvals, yvals, yerr=yerr)
    plt.legend()
    plt.xlabel('Distance walked (L)')
    plt.ylabel('Probability density (1/L)')
    plt.suptitle('Probabiltiy of walk lengths')
    plt.title('N = 32')

    plt.savefig('figs/exactPDF.pdf')
    funmath.toc()
    sum2 = 0
    # for i,j  in zip(yvals,y[:len(yvals)]):
    #     sum2 += np.sqrt(i*i + j*j)
    # print(sum2)
    plt.show()
    # print(sum(y))
    ###########################################################################

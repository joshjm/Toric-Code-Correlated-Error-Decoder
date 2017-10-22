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
    s = range( (N-L)/2,      (N+L)/2+1,  1) #range doesnt include end point
    p = range( (N-L)/2+1,    (N+L)/2,    1)
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

    for N in [8,16,32,64]:
        #print(Prob(N,L))
        x = [2*i for i in range(N/2+1)]
        y = [Prob(N,L) for L in x]
        plt.plot(x,y, marker =marker.next(), label  = 'N = '+str(N))
    ###########################################################################

    #plt.errorbar(xvals, yvals, yerr=yerr)
    plt.legend()
    plt.xlabel('Distance walked (L)')
    plt.ylabel('Probability density (1/L)')
    plt.suptitle('Probabiltiy of walk lengths')
    plt.title('Exact PDF calculation')

    plt.savefig('figs/exactPDFdemo.pdf')
    funmath.toc()
    sum2 = 0
    plt.show()
    print(sum(y))
    ###########################################################################

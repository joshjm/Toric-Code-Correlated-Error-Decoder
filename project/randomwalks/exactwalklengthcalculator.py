import walks
import numpy as np
import funmath
import math
from scipy.stats import gamma

file = open('exactexpectedlengths.txt','w')

def nCr(n,r):
    f = math.factorial
    return f(n) / f(r) / f(n-r)
def manhat_distance(i,j,N):
    x_rot = (2*i-N)/np.sqrt(2) + (2*j-N)/np.sqrt(2)
    y_rot = -(2*i-N)/np.sqrt(2) + (2*j-N)/np.sqrt(2)
    return((abs(x_rot)+abs(y_rot))/np.sqrt(2))

def pythag_distance(i,j,N):
    return(math.sqrt(pow(2*i-N,2)+pow(2*j-N,2))*math.sqrt(2)/2)

def walklengthcalc(N):
    #funmath.tic()
    pythag_sum = 0
    manhat_sum = 0
    for i in range(N+1):
        for j in range(N+1):
            pythag_disp = pythag_distance(i,j,N)
            manhat_disp = manhat_distance(i,j,N)

            combinations = nCr(N,i)*nCr(N,j)
            pythag_sum += pythag_disp*combinations
            manhat_sum += manhat_disp*combinations
        ##testing
        #    file.write("("+str(displacement)+", "+str(combinations)+")"+"   ")
        #file.write("\n")

    total_number_of_possible_moves = pow(4,N)
    pythag_expected = pythag_sum/total_number_of_possible_moves
    manhat_expected = manhat_sum/total_number_of_possible_moves
    #print('N = '+str(N))
    #print('pythag expected distance: '+str(pythag_expected))
    #print('manhat expected distance: '+str(manhat_expected))
    file.write(str(N)+','+str(pythag_expected)+','+str(manhat_expected)+'\n')
    #funmath.toc()
    return([pythag_expected, manhat_expected, np.sqrt(N)])
if __name__ =="__main__":
    lengths = walklengthcalc(32)
    print(' pythag = '+str(lengths[0])+ '\n rt(N) = '+str(lengths[2])+' \n manhat = '+str(lengths[1]) )

    #gamma distribution stuff
    file = open('gamma_info.txt','w')
    loops = 1000000
    N=32
    rawdata = np.loadtxt('manhat_pythag_data.txt' ,  delimiter=',', skiprows=0, unpack=False)

    manhat_data = rawdata[:,0]
    pythag_data = rawdata[:,1]

    #fit a gamma distribution
        #to the pythag data
    pythag_fit_alpha, pythag_fit_loc, pythag_fit_beta = gamma.fit(pythag_data)
    pythag_dist = gamma(pythag_fit_alpha, pythag_fit_loc, pythag_fit_beta )
        #to the manhat data
    manhat_fit_alpha, manhat_fit_loc, manhat_fit_beta = gamma.fit(manhat_data)
    manhat_dist = gamma(manhat_fit_alpha, manhat_fit_loc, manhat_fit_beta )
    #save info
    [pa,pl,pb] = [pythag_fit_alpha, pythag_fit_loc, pythag_fit_beta]
    [ma,ml,mb] = [manhat_fit_alpha, manhat_fit_loc, manhat_fit_beta]
    file.write(str(pythag_fit_alpha)+','+ str(pythag_fit_loc)+',' + str(pythag_fit_beta)+'\n')
    file.write(str(manhat_fit_alpha)+','+ str(manhat_fit_loc)+',' + str(manhat_fit_beta)+'\n')
    funmath.toc()

    candidates = open('candidates.txt','w')
    print('pythag, rt(N), manhat, manhat_gamma_max, py_gamma_max')
    print([lengths[0], lengths[2], lengths[1], (ma-1.0)*mb+ml, (pa-1.0)*pb+pl])
    candidates.write('pythag, rt(N), manhat, manhat_gamma_max, py_gamma_max \n')
    candidates.write(str([lengths[0], lengths[2], lengths[1], (ma-1.0)*mb+ml, (pa-1.0)*pb+pl ])) #*b because its actuall theta!

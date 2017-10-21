import walks
import numpy as np
import funmath
import math
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
steps = int(input('walk length: '))
lengths = walklengthcalc(steps)
print(' pythag = '+str(lengths[0])+ '\n rt(N) = '+str(lengths[2])+' \n manhat = '+str(lengths[1]) )

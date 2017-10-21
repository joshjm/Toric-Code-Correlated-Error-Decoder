import walks
import numpy as np
import funmath
import math
file = open('expectedlengths.txt','w*')
def gamma(n):
    return(math.factorial(n-1))

for CorrLen in [32]:#range(32+1):
    funmath.tic()
    L = 2*CorrLen + 1
    array = np.zeros((2*L,2*L))
    results = np.zeros((2*L,2*L))
    loops = 10000
    distsum = 0
    for i in range(loops):
        returned = walks.type4(array,L,CorrLen)
        displacement = [returned[0], returned[1]]
        endpoint = [returned[2], returned[3]]
        distsum += np.sqrt(pow(displacement[0],2)+pow(displacement[1],2))
        #[walk[-1][0] - walk[0][0],walk[-1][1] - walk[0][1]]
        results[endpoint[0],endpoint[1]] += 1

        #results[endpoint[0],endpoint[1]] += 1
    # for i in range(L):
    #     for j in range(L):
    #         file.write(str(results[i][j]/loops)+",    ")
    #     file.write("\n")
    expected = distsum/loops
    print(str(CorrLen)+" expected walk length is: "+ str(expected))
    #dim = 2 #number of dimensions
    #exact = np.sqrt(2*CorrLen/dim)*gamma((dim+1.0)/2.0)/gamma(dim/2)
    #print(exact)
    print(math.sqrt(CorrLen))
    file.write(str(CorrLen)+','+str(expected)+'\n')
    funmath.toc()

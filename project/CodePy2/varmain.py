
#import importlib
import numpy as np
import random
#import matplotlib.pyplot as plt
import subprocess
import os
import funmath
import sys
import multiprocessing as mp
import datetime
import uuid
import collections
import scipy.stats as sp

import traceback #allows me to get all err info while in MT & try.
#import hanging_threads
from extra.blossom5 import pyMatch
#from hanging_threads import start_monitoring#use to check for thread stalls
#monitoring_thread = start_monitoring(seconds_frozen=10, test_interval=100)
"""
This code will generate qubits, apply error to them, measure the syndrome of the
error, find the least weight matching of the error, and find paths between those
matchings. It will loop over this to determine the failure rate for different
lattice configurations.

This code is multithreaded. It is hardcoded to work on the
@smp-comp-03.smp.uq.edu.au server. Only major modification that would need to be
done to work elsewhere is changing the write directory from the RAM disk
/dev/shm and change the local dir.
- writing to ramdisk halves comp time.

This code is modified to run with a chosen set of error rates and corrlens.
--do via a list and dictionary?

-halfway through converting to use Naomi Nickersons code to interface with
 BlossomV code. Hardcoded to run on dogmatix server. I may need to copy her
 whole blossom folder? something about PMlib
 -note that /dev/shm is a temp file system for any unix like system. --ie speeds
  up passing data between programs

need to create a drive/RAMDisk called ramdisk when running on a mac.
Unix has /dev/shm

"""
global maxqueue

def worker(L, length, strength, variance, loops, errtype, CorrLen, rawerror, adjust):
    sum1 = 0 #sum of qubit failures
    sum2 = 0
    for loop_it in range(loops):
        try:
            pid =str(os.getpid()) #unique ID for each parallel process
            if not (rawerror - int(rawerror) == 0):# if not an integer
                rand = random.random()
                frac = (rawerror - int(rawerror))
                if rand < frac:#randomly choose above and below to get ok average
                    ErrorNum = int(rawerror) +1
                else:
                    ErrorNum = int(rawerror)
            else:
                ErrorNum = rawerror
            #create the qubit arrays -- Lx2xL array
            blankarray = funmath.createarray(L,L) #LxL grid.


            #Apply X errors (E) to the qubits
            ErrorArray = funmath.ApplyXErrors(ErrorNum,np.array(blankarray),errtype,L, CorrLen)
            #Generate syndrome
            PSyndrome = funmath.Measure_Syndrome(ErrorArray,L,L)
            #search through syndrome and add defects to a list
                #Could make this part of the syndrome measurement
            vertices = funmath.FindDefects(PSyndrome)
            if len(vertices)==0:
                continue #if no errors detected, move to next loop

            #Find Manhatten distance
            zM = funmath.Manhatten_Distance(vertices,L,L)

            if adjust == 'gauss':
              #adjust for correlated errors
              zM = funmath.adjustmatrix_gaussian(zM, length, L, strength, variance)
            elif adjust == 'pythag':
              zM = funmath.adjustmatrix_gamma_pythag(zM)
            elif adjust == 'manhat':
              zM = funmath.adjustmatrix_gamma_manhat(zM)


            #Creating the TSPLIB file
                #Parameters for TSPLIB file
            graph=[]
                #write manhatten distances
            for row in range(0,len(zM[:,0])-1):
                for col in range(row+1,len(zM[:,0])):
                    graph.append([row,col,int(zM[row,col])])

            #Creating the TSPLIB file
                #Parameters for TSPLIB file
            #RAMdisk

            prefix = '/dev/shm/'
            open(prefix+'blossominput'+pid+'.txt', 'w').close() #clear the file
            with open(prefix+"blossominput"+pid+".txt", 'a') as f: #write new data to file
                    #write number of nodes and edges
                f.write(str(len(zM[:,0])) + ' ' + str(int(len(zM[:,0])*(len(zM[:,0])-1)/2))+'\n')
                count =1
                    #write manhatten distances
                for row in range(0,len(zM[:,0])-1):
                    for col in range(row+1,len(zM[:,0])):
                        f.write(str(row)+' '+str(col)+' '+str(int(zM[row,col]))+'\n')
                f.close()
                #the next two lines suppress the output of calling the blossom code

            FNULL = open(os.devnull, 'w')
            #location of the made src, with python file from nickerson
            retcode = subprocess.call(["CodePy2/extra/blossom5/blossom5", "-e",prefix+"blossominput"+pid+".txt","-w",prefix+"blossomoutput"+pid+".txt"], stdout=FNULL, stderr=subprocess.STDOUT)
            matching = open(prefix+"blossomoutput"+pid+".txt", 'r') #open the putput of the blossom5 code
            matches = matching.readlines() #read the matches
            matching.close()
            os.system('rm '+prefix+'blossominput'+pid+'.txt')
            os.system('rm '+prefix+'blossomoutput'+pid+'.txt')
            #process blossom output
            pairs = []
            for i in range(len(matches)):
                if i == 0:
                    continue
                matches[i] = matches[i].strip()
                pairs.append(matches[i].split(' '))
                for j in range(2):
                    pairs[i-1][j] = int(pairs[i-1][j])
            #################################################
            #create an array counting up
                #this is better done with a dict
            refarray = np.zeros((L,L))
            refdict={}
            counter = 1 #counter could be repalced by i+j
            for i in range(len(refarray[:,0])):
                for j in range(len(refarray[0,:])):
                    refarray[i,j] = counter
                    refdict[counter] =[i,j]
                    counter +=1
            #calculating paths
            ## #my algorithm - VERY FAST
            paths = []
            for i in pairs:
                p1 = list(vertices[i[0]])
                p2 = list(vertices[i[1]])
                paths.append(funmath.CustomShortestPath(p1,p2,L,L))

            #now we convert the paths into the actual bits that get flipped
            CorrectionArray = funmath.GetFlippedPoints2(paths,blankarray) #may stay as 2, as its the correction grid/syndrome

            #now we apply the corrections
            CorrectedArray = np.multiply(ErrorArray,CorrectionArray)
            CorrectedArray = np.array(CorrectedArray)

            #now we test for a failure
            qubit1 = 1
            qubit2 = 1
            for i in CorrectedArray[0,0,:]:
                qubit1 = qubit1*i

            for i in CorrectedArray[:,1,0]:
                qubit2 = qubit2*i
            if qubit1 == -1: #counts all the failures
                sum1 += 1
            if qubit2 == -1:
                sum2 += 1

        except Exception as e:
            print("exception!")
            #errors.put(e)
            errors.put(sys.exc_info())
    loopdata.put([L, length, strength, variance, rawerror, CorrLen, adjust, 1.0*sum1/loops, 1.0*sum2/loops])
    print([L, length, strength, variance, rawerror, CorrLen, adjust, 1.0*sum1/loops, 1.0*sum2/loops])

    sys.stdout.flush() #this is needed otherwise the output will be
           #stored in a buffer and not written to nohup.out


if __name__ == '__main__':
    funmath.clear_all()
    funmath.tic() #start timer
    print(str(datetime.datetime.now().isoformat()))
    parameters = [] #if length(parameters) grows too large, then the pipes get full for the queue.
    """ set the correlation distance N and the number of anyons here
        NOTE they need to be the same length to be combined in combined"""
    N = [32] #32 steps has expected walk length of 5.016
    anyons = [15]
    combined = [[N[i], anyons[i]] for i in range(len(N))]
    outer_loops = 1
    """ how many times to repeat for each set of values. allows you to
        multithread each single value. set to high, if mostly running
        for a single value to optimized speed. set lower if many
        different sets of parameters are being run. """

    inner_loops = 10000
    """ essentially sets the accuracy of the failure rate for each
        set of parameters. the pipe can get full if set too high.
        try to catch failure if going above 500. """

    #create the values to apply_async over
    for repeat in range(outer_loops): #set how many threads to set for each value.
        for codesize in [40]:
            for errtype in [4]:
                for strength in [1]:
                    for variance in np.arange(11, 13, 0.1):
                        for adjust in ['gauss']:
                            for pair in combined:
                                for expectedlength in np.arange(4.5, 5.5 , 0.05):
                                    #create an array of parameters, and then apply all at once
                                    parameters.append([codesize,expectedlength,strength,variance,inner_loops,errtype,pair[0],pair[1],adjust])

    #create a dict to recombine all the data from loops
    datadict = collections.defaultdict(float) #float and defaultdict together initialze missing key values to zero

    maxq = 300 #determines how big the queue gets. tested to fail over 325.
    maxrange = len(parameters)/maxq + 1
    counter = 0
    for subparams in [parameters[i*maxq:i*maxq+maxq] for i in range(0,maxrange)]: #need to reduce total size, so queue doesnt get full.

        print(str(100.0*counter/maxrange)+' % done ' )
        ###################################
        #set up the multiprocessing
        global errors
        global loopdata
        progress = 0
        errors = mp.Queue(0) #return errors
        loopdata = mp.Queue(0) #stores each loops data
        #threadcount = mp.cpu_count() -1
        threadcount = 325 #len(parameters) #careful
        pool = mp.Pool(processes = threadcount) #to create multiple processes
        for config in subparams:
            #apply multithreading  [L,length,strength,variance,loops,errtype,combined,CorrLen,rawerror,adjust]
            processors = pool.apply_async(worker, config)
        pool.close()
        pool.join()

        #empty the queue
        while loopdata.qsize() != 0:
            got = loopdata.get()
            datadict[tuple(got[:6+1])] += 1.0*(got[7] + got[8])/(2*outer_loops)
        counter +=1
        while errors.qsize() != 0: #error reporting
            print("EXCEPTION")
            print(str(errors.get()))

    ###################################

    #save the data
    filename = ('./CodePy2/data/highMT_l_'+str(int(outer_loops*inner_loops))+'_'+uuid.uuid4().hex)
    data = open(filename + ".txt", 'w')
    print('L, w_bar, strength, sigma_sq, anyons, N, p_failure')
    data.write('L, w_bar, strength, sigma_sq, anyons, N, p_failure \n')
    for i in datadict:
        #print data
        print(str(i)+str(datadict[i]))
        #save to file
        for j in i:
            data.write(str(j)+', ')
        data.write(str(datadict[i])+'\n')

    print(str(datetime.datetime.now().isoformat()))
    funmath.toc()

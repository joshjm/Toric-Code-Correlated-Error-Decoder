
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
import traceback #allows me to get all err info while in MT & try.
from extra.blossom5 import pyMatch
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
funmath.clear_all()

def main(codesize):
    ####### MAIN PARAMS ###############
    mt = True #turn multithreading on/off
    global mac
    mac = False #switch between /dev/shm and macs ramdisk
    '''range of expected lengths to cycle over for testing correction'''
    expectedlengths = range(codesize/2)
    '''code size'''
    global L
    L = codesize #set codesize in init
    '''Enter details for how hard to adjust for correlations'''
      # What is the expected error correlation distace
    global adjust #flag for whether or not to apply `smart' correction.
    adjust = False
    print("adjust = "+str(adjust))
    strength = 1    # eg; strength = 0.2 means 20% reduction in distance
    variance = 1        # how wide the adjustment is
    '''number of loops'''
    loops = 100
    '''number of threads'''
    threadcount = 2
    '''correlation length'''

    '''errrate range'''

    '''Error type'''
    errtype = 6
    ###################################
    '''input type'''

    #errs = [200,100,66.66,50,40,33.33,28.57,25,22.22,20]# anyon number
    #corrs = [2,4,6,8,10,12,14,16,18,20] #correlation lengths

    corrs = [192] #32 steps has expected walk length of 5
    errs = [1 for i in corrs]

    ##set the range of error rates to scan over
    #ErrRates = 0.05*np.ones(10)
    #corrs = np.arange(1,11,1)

    #errs = [i*L*L for i in ErrRates]
    #corrs = [4]
    #errs = [4]

    combined = [[corrs[i], errs[i]] for i in range(len(corrs))]


    ###################################
    global quick
    quick = 1
    global m   #height
    m = L
    global n
    n = L   #width

    #loops = int(input('Choose number of loops: '))

    funmath.tic()

    #set up the multiprocessing
    global output #does a queue need to be global?
    global errors
    errors = mp.Queue(0) #return errors
    output = mp.Queue(0) #to store data before sorting

    pool = mp.Pool(processes = threadcount) #to create multiple processes
    outlist = []

    if mt:
        print('multithreading enabled')
        print(' anyons, CorrLen, q1 failure, q2 failure, Avg man dist, Avg Match Dist')
        for i in combined:
          for length in expectedlengths:
            processes = pool.apply_async(worker, [ L, length, strength, variance, loops, errtype, i, len(combined),mt])
        pool.close()
        pool.join()
        #report errors
        while errors.qsize() != 0:
            print(str(errors.get()))
        while output.qsize() != 0: #calling get reduces the size of queue
            got = output.get()
            outlist.append(got)
        outlist = sorted(outlist, key =lambda item: item[6])
    else:
        print('multhreading disabled')
        print(' anyons, CorrLen, q1 failure, q2 failure, Avg man dist, Avg Match Dist')

        for i in combined:
          for length in expectedlengths:
            returned_value = worker(  L,length,strength,variance,loops,errtype,i,len(combined),mt)
            outlist.append(returned_value)

            #take the queue, and put into a list
    #write the sorted output to file
    filename = ('./CodePy2/data/'+'l'+str(loops)+'L'+str(L)+uuid.uuid4().hex)
    data = open(filename + ".txt", 'w')
    data.write(' anyons '+',' + ' CorrLen ' +','+ ' q1 failure '+','+' q2 failure '+', Avg man dist'+', Avg Match Dist, expected len'+'\n')

    for k in outlist:
        data.write(str(k[0])+',    ' + str(k[1]) +',    '+ str(k[2])+',    '+str(k[3])+ ',    '+str(k[4])+',    '+str(k[5])+',    '+str(k[6])+'\n')

def worker(L,expectedlength,strength,variance,loops,errtype,combined,errlen, mt):
    try:
        pid =str(os.getpid()) #unique ID for each parallel process

        rawerror = combined[1] #number of error sites
        CorrLen = combined[0] #correlation length
        avgmatch = 0
        total1 = 0 #store failures/success
        total2 = 0
        zMTotal = 0 #store manhatten distance
        matchtotal = 0 #store match distance
        for loopcounter in range(loops):
            if not (rawerror - int(rawerror) == 0):# if not an integer
                rand = random.random()
                frac = (rawerror - int(rawerror))
                if rand < frac:#randomly choose above and below to get ok average
                    ErrorNum = int(rawerror) +1
                else:
                    ErrorNum = int(rawerror)
            else:
                ErrorNum = rawerror
            #create the qubit arrays
            blankarray = funmath.createarray(m,n)

            #Apply X errors (E) to the qubits

            ErrorArray = funmath.ApplyXErrors(ErrorNum,np.array(blankarray),errtype,L, CorrLen)

            #debug err arrays

            #Generate syndrome
            PSyndrome = funmath.Measure_Syndrome(ErrorArray,m,n)
            #search through syndrome and add defects to a list
                #Could make this part of the syndrome measurement
            vertices = funmath.FindDefects(PSyndrome)
            #check if any errors need fixing

            if len(vertices)==0:
                continue#if not, then move on.
                    #Find Manhatten distance

            zM = funmath.Manhatten_Distance(vertices,m,n)

            if adjust:
              #adjust for correlated errors
              zM = funmath.adjustmatrix(zM, expectedlength, L, strength, variance)

            #Creating the TSPLIB file
                #Parameters for TSPLIB file
            graph=[]
                #write manhatten distances
            for row in range(0,len(zM[:,0])-1):
                for col in range(row+1,len(zM[:,0])):
                    graph.append([row,col,int(zM[row,col])])
            ###################################################
            ##This uses Nickerson's code. CURRENTLY BROKEN
            # #call the blossom5 code on the generated syndrome
            #
            # matching = pyMatch.getMatching(len(vertices),graph)
            # #process nickerson output
            # pairs = []
            # for i in range(0,len(matching),2):
            #     pairs.append([matching[i],matching[i+1]])
            #
            ##################################################
            #Creating the TSPLIB file
                #Parameters for TSPLIB file
            #RAMdisk?
            if mac:
                prefix = '/Volumes/RAM Disk/'
            else:
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
            retcode = subprocess.call(["CodePy2/extra/blossom5-v2.05.src/blossom5", "-e",prefix+"blossominput"+pid+".txt","-w",prefix+"blossomoutput"+pid+".txt"], stdout=FNULL, stderr=subprocess.STDOUT)
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
            ##################################################
            #create an array counting up
                #this is better done with a dict
            refarray = np.zeros((m,n))
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
            pathlen = 0
            for i in pairs:
                p1 = list(vertices[i[0]])
                p2 = list(vertices[i[1]])
                paths.append(funmath.CustomShortestPath(p1,p2,m,n))
                pathlen += len(paths[-1]) - 1 #-1 becasue endpoints
            #errors.put(len(pairs))
    	    #custompath.append(funmath.CustomShortestPath(p1,p2,m,n))
            avgmatch += 1.0*pathlen/len(pairs)
            #paths = custompath

            #now we convert the paths into the actual bits that get flipped
            CorrectionArray = funmath.GetFlippedPoints2(paths,blankarray)

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

            if qubit1 == -1:
                total1+=1
            if qubit2 ==-1:
                total2+=1
            zMTotal += np.mean(zM)
            #matchtotal +=
    ###########################
            ##print the graphical output
            #funmath.ploterror(ErrorArray,PSyndrome,paths,vertices,CorrectionArray)


        zMavg = 1.0*zMTotal/loops
        if mt:
            queuelen = int(output.qsize())
            #print (str([rawerror, CorrLen, 1.0*total1/loops, 1.0*total2/loops,zMavg,avgmatch/loops])+'   % done = '+str(100.0*(queuelen)/(maxcorr-mincorr+1)/stepcorr/errlen)+'    '+str(datetime.datetime.now().isoformat())) #step err has int errors. this counter isnt accurate.
            #print (str([rawerror, CorrLen, 1.0*total1/loops, 1.0*total2/loops,zMavg,avgmatch/loops,expectedlength])+'      '+str(datetime.datetime.now().isoformat())) #step err has int errors. this counter isnt accurate.

            output.put([rawerror, CorrLen, 1.0*total1/loops, 1.0*total2/loops,zMavg,avgmatch/loops,expectedlength])
            sys.stdout.flush() #this is needed otherwise the output will be
                   #stored in a buffer and not written to nohup.out
        else:
            return([rawerror, CorrLen, 1.0*total1/loops, 1.0*total2/loops,zMavg])
    except Exception:
      print("exception")
      print(traceback.print_exc())


if __name__ == '__main__':
    #os.system('mkdir /dev/shm/s4318965/')
    print(str(datetime.datetime.now().isoformat()))
    for codesize in [10]:
        main(codesize)
    #os.system('rm -rf /dev/shm/s4318965/')
    print(str(datetime.datetime.now().isoformat()))
    print('Code Complete')
funmath.toc()


#import importlib
import numpy as np
import random
#import matplotlib.pyplot as plt
import subprocess
import os
import funmath
import sys
import multiprocessing as mp

"""
This code will generate qubits, apply error to them, measure the syndrome of the
error, find the elase weight matching of the error, and find paths between those
matchings.

"""
funmath.clear_all()

#importlib.reload(funmath) #if i edit the plotting function, i need to reload it or else update have no effect

#Input parameters
    # m*n chooses the number of plaquette  stabiliers (physical qubits =m*n*2 )
#TEST PARAM
######################

def main():
    #quick = int(input('run quick? (0,1):'))
    global L
    L = 25
    global quick
    quick = 1
    global m   #height
    m = L
    global n
    n = L   #width
    loops = 1000
    #loops = int(input('Choose number of loops: '))
    errtype=5

    funmath.tic()
    os.chdir("/home/s4318965/CodePy2")
    #set up the loop
    ######################
    '''errrate range'''
    global minerr
    minerr = 0.05
    global maxerr
    maxerr = 0.5
    global steperr
    steperr = 0.025
    ######################
    global output
    output = mp.Queue(0)
    #pool = mp.Pool(processes=24)
    pool = mp.Pool(processes = 11)

    #for ErrorRate in np.arange(minerr,maxerr+steperr,steperr):
    ErrRates = np.arange(minerr,maxerr+steperr,steperr)
    errlen = len(ErrRates)
    try:
        for ErrorRate in ErrRates:
            processes = pool.apply_async(worker, [ L,loops,errtype,ErrorRate,errlen])
        pool.close()
        pool.join()
    except KeyboardInterrupt:
        pool.terminate()
        pool.join()
    outlist =[]
    while output.qsize() != 0: #calling get reduces the size of queue
        got = output.get()
        outlist.append(got)
    outlist.sort()

    filename = ('data/'+'l'+str(loops)+'L'+str(L))
    data = open(filename + ".txt", 'w')
    data.write(' anyons '+',' + ' CorrLen ' +','+ ' q1 failure '+','+' q2 failure '+'\n')

    for k in outlist:
        data.write(str(k[0])+',    ' + str(k[1]) +',    '+ str(k[2])+',    '+str(k[3]) +'\n')

def worker(L,loops,errtype,ErrorRate,errlen):
    pid =str(os.getpid()) #unique ID for each parallel process
    if errtype==5:
        er = ErrorRate
        ErrorRate = int(ErrorRate*L*L) #convert to number of errors
    ############################
    '''corr len range'''
    mincorr = 1
    #maxcorr = 10
    maxcorr = 10
    stepcorr = 1
    ############################
    ramloc = '/dev/shm/s4318965/' #ramdisk location
    for CorrLen in range(mincorr,maxcorr+stepcorr,stepcorr):#length of correlation
        '''if CorrLen*ErrorRate >= L*L/2: #skip any with too much error
            continue'''
        total1 = 0
        total2 = 0
        for loopcounter in range(loops):
            #print(' %done = '+str(100*((er-steperr)/(maxerr)+(CorrLen-stepcorr)*steperr/(maxcorr))), end='\r') #step err has int errors. this coutner isnt accurate.
            #sys.stdout.write("\r amount done: %s" % str(100*((er-steperr)/(maxerr)+(CorrLen-stepcorr)*steperr/(maxcorr))))
            #sys.stdout.flush()
            #create the qubit array

            blankarray = funmath.createarray(m,n)

            #Apply X errors (E) to the qubits

            ErrorArray = funmath.ApplyXErrors(ErrorRate,np.array(blankarray),errtype,L, CorrLen)

            #Generate syndrome
            PSyndrome = funmath.Measure_Syndrome(ErrorArray,m,n)

            #search through syndrome and add defects to a list
                #Could make this part of the syndrome measurement
            vertices = funmath.FindDefects(PSyndrome)

            if len(vertices) > 0 : #test to make sure there are any actions needed to be performed
                    #Find Manhatten distance
                zM = funmath.Manhatten_Distance(vertices,m,n)
                #Creating the TSPLIB file
                    #Parameters for TSPLIB file

                with open(ramloc+"blossominput"+pid+".txt", 'w') as f: #write new data to file
                        #write number of nodes and edges
                    f.write(str(len(zM[:,0])) + ' ' + str(int(len(zM[:,0])*(len(zM[:,0])-1)/2))+'\n')
                    count =1
                        #write manhatten distances
                    for row in range(0,len(zM[:,0])-1):
                        for col in range(row+1,len(zM[:,0])):
                            f.write(str(row)+' '+str(col)+' '+str(int(zM[row,col]))+'\n')
                    f.close()
                ##call the blossom5 code on the generated syndrome.
                    #the next two lines suppress the output of calling the blossom code
                FNULL = open(os.devnull, 'w')
                retcode = subprocess.call(["extra/blossom5-v2.05.src/blossom5", "-e",ramloc+"blossominput"+pid+".txt","-w",ramloc+"blossomoutput"+pid+".txt"], stdout=FNULL, stderr=subprocess.STDOUT)
                matching = open(ramloc+"blossomoutput"+pid+".txt", 'r') #open the putput of the blossom5 code
                matches = matching.readlines() #read the matches
                matching.close()
                os.system('rm '+ramloc+'blossominput'+pid+'.txt')
                os.system('rm '+ramloc+'blossomoutput'+pid+'.txt')
                #process blossom output
                pairs = []
                for i in range(len(matches)):
                    if i == 0:
                        continue
                    matches[i] = matches[i].strip()
                    pairs.append(matches[i].split(' '))
                    for j in range(2):
                        pairs[i-1][j] = int(pairs[i-1][j])

                #create an array counting up
                    #this is better done with a dict
                refarray = np.zeros((m,n))
                refdict={}
                counter = 1
                for i in range(len(refarray[:,0])):
                    for j in range(len(refarray[0,:])):
                        refarray[i,j] = counter
                        refdict[counter] =[i,j]
                        counter +=1
            #calculating paths
                ## #my algorithm - VERY FAST

                custompath=[]

                for i in pairs:
                    p1 = list(vertices[i[0]])
                    p2 = list(vertices[i[1]])
                    custompath.append(funmath.CustomShortestPath(p1,p2,m,n))

                paths = custompath

                #now we convert the paths into the actual bits that get flipped
                CorrectionArray = funmath.GetFlippedPoints(paths,blankarray)

                if quick == 0:
                    #print whats happening
                    funmath.ploterror(ErrorArray,PSyndrome,paths,vertices,CorrectionArray)

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

        #print('Error rate =' +str(ErrorRate))
        #print('q1 failure rate = '+str(total1/loops))
        #print('q2 failure rate = '+str(total2/loops))

        #writes failure rate
        queuelen = int(output.qsize())
        sys.stdout.write('\r approx % done = '+str(100.0*(queuelen)/(maxcorr-mincorr+1)/stepcorr/errlen)+'     ') #step err has int errors. this counter isnt accurate.

        sys.stdout.flush()

        output.put([ErrorRate, CorrLen, 1.0*total1/loops, 1.0*total2/loops])

if __name__ == '__main__':
    os.system('mkdir /dev/shm/s4318965/')
    main()
    os.system('rm -rf /dev/shm/s4318965/')
funmath.toc()

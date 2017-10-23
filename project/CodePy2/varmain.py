
import numpy as np
import random
import subprocess
import os
import funmath
import sys
import multiprocessing as mp
import datetime
import uuid
import collections
import traceback  # allows me to get all err info while in MT & try.
from extra.blossom5 import pyMatch

"""
cd cwd/Toric-Code-Correlated-Error-Decoder/project/

This code emulates a grid of qubits and generates errors using either a
correlated error model or uncorrelated error model on it. It then applys a
matching algoritm of either least weight perfect matching (performed by
blossom5) or one of several novel `improved decoders' for improved qubit
recovery rates, when the correlated noise model is used.

To use this code; extract blossom5-v2.05.src from CodePys2/extra to
CodePys2/extra/blossom5 and call make from that directory.
Calling `python CodePy2/varmain.py' should then work.
A drive called /dev/shm/ must exist (RAM drive on Unix-like systems) for
passing information to Blossom5.

If using gamma distributions, make sure to update the hardcoded
[alpha, loc, beta] values in funmath.adjustmatrix
"""

def worker(L, length, strength, variance, loops,
           errtype, CorrLen, anyons, adjust):
    sum1 = 0  # sum of qubit failures
    sum2 = 0
    for loop_it in range(loops):
        try:
            if not (anyons - int(anyons) == 0):  # if not an integer
                rand = random.random()
                frac = (anyons - int(anyons))
                if rand < frac:  # Fractionally choose vals to average.
                    ErrorNum = int(anyons) + 1
                else:
                    ErrorNum = int(anyons)
            else:
                ErrorNum = anyons
            # create the qubit arrays -- Lx2xL array
            blankarray = funmath.createarray(L, L)  # LxL grid.

            # Apply X errors (E) to the qubits
            ErrorArray = funmath.ApplyXErrors(
                ErrorNum, np.array(blankarray), errtype, L, CorrLen)
            # Generate syndrome
            PSyndrome = funmath.Measure_Syndrome(ErrorArray, L, L)

            # Search through syndrome and add defects to a list
            vertices = funmath.FindDefects(PSyndrome)
            if len(vertices) == 0:
                continue  # If no errors detected, move to next loop.

            # Find Manhatten distance
            zM = funmath.Manhatten_Distance(vertices, L, L)
            # choose corection method

            # Adjust distances for new correction weighting.
            zM = funmath.adjustmatrix(
                zM, length, L, strength, variance, adjust)

            #Creating the TSPLIB file for blossomV
                # Parameters for TSPLIB file
            graph = []
            # Begin passing information to blossomV
            for row in range(0, len(zM[:, 0]) - 1):
                for col in range(row + 1, len(zM[:, 0])):
                    graph.append([row, col, int(zM[row, col])])

            prefix = '/dev/shm/'
            pid = str(os.getpid())

            with open(prefix + "blossominput" + pid + ".txt", 'w') as f:
                    # write number of nodes and edges
                f.write(str(
                    len(zM[:, 0])) + ' ' + str(int(len(zM[:, 0]) * (len(zM[:, 0]) - 1) / 2)) + '\n')
                count = 1
                # write manhatten distances
                for row in range(0, len(zM[:, 0]) - 1):
                    for col in range(row + 1, len(zM[:, 0])):
                        f.write(str(row) + ' ' + str(col) + ' ' +
                                str(int(zM[row, col])) + '\n')
                f.close()

            # Suppress blossom terminal output
            FNULL = open(os.devnull, 'w')
            # location of the made src, with python file from Nickerson
            retcode = subprocess.call(
                [
                    "CodePy2/extra/blossom5/blossom5",
                    "-e",
                    prefix +
                    "blossominput" +
                    pid +
                    ".txt",
                    "-w",
                    prefix +
                    "blossomoutput" +
                    pid +
                    ".txt"],
                stdout=FNULL,
                stderr=subprocess.STDOUT)
            # open the output of the blossom5 code
            matching = open(
                prefix + "blossomoutput" + pid + ".txt",
                'r')
            matches = matching.readlines()  # read the matches
            matching.close()
            # clean up/ free ram
            os.system('rm ' + prefix + 'blossominput' + pid + '.txt')
            os.system('rm ' + prefix + 'blossomoutput' + pid + '.txt')
            # process blossom output
            pairs = []
            for i in range(len(matches)):
                if i == 0:
                    continue
                matches[i] = matches[i].strip()
                pairs.append(matches[i].split(' '))
                for j in range(2):
                    pairs[i - 1][j] = int(pairs[i - 1][j])
            #create paths between matched qubits
            refarray = np.zeros((L, L))
            refdict = {}
            counter = 1  # counter could be repalced by i+j
            for i in range(len(refarray[:, 0])):
                for j in range(len(refarray[0, :])):
                    refarray[i, j] = counter
                    refdict[counter] = [i, j]
                    counter += 1
            # calculating paths
            paths = []
            for i in pairs:
                p1 = list(vertices[i[0]])
                p2 = list(vertices[i[1]])
                paths.append(funmath.CustomShortestPath(p1, p2, L, L))

            # now we convert the paths into the actual bits that get flipped
            CorrectionArray = funmath.GetFlippedPoints2(paths, blankarray)

            # now we apply the corrections
            CorrectedArray = np.multiply(ErrorArray, CorrectionArray)
            CorrectedArray = np.array(CorrectedArray)

            # now we test for a failure
            qubit1 = 1
            qubit2 = 1
            for i in CorrectedArray[0, 0, :]:
                qubit1 = qubit1 * i
            for i in CorrectedArray[:, 1, 0]:
                qubit2 = qubit2 * i

            # counts all the failures
            if qubit1 == -1:
                sum1 += 1
            if qubit2 == -1:
                sum2 += 1

        except Exception as e:
            print("exception!")
            errors.put(sys.exc_info())
            #errors.put(e)
            print(e)
    # Put result into threadsafe queue
    loopdata.put([L, length, strength, variance, anyons, CorrLen,
                  adjust, 1.0 * sum1 / loops, 1.0 * sum2 / loops])
    print([L, length, strength, variance, anyons, CorrLen,
           adjust, 1.0 * sum1 / loops, 1.0 * sum2 / loops])

    sys.stdout.flush()  # this is needed otherwise the output will be
    # stored in a buffer and not written to nohup.out/ out.out


if __name__ == '__main__':
    funmath.clear_all()
    funmath.tic()  # start timer
    print(str(datetime.datetime.now().isoformat()))
    # if len(parameters) grows too large, then the pipes get full for the
    # queue.
    parameters = []
        # set the correlation distance N and the number of anyons here
        #    NOTE they need to be the same length to be combined in combined
    N = [32,32,32]  # 32 steps has expected walk length of 5.016
    anyons = [8,12,16]
    combined = [[N[i], anyons[i]] for i in range(len(N))]
    outer_loops = 100
        # how many times to repeat for each set of values. allows you to
        # multithread each single value. set to high, if mostly running
        # for a single value to optimized speed. set lower if many
        # different sets of parameters are being run.

    inner_loops = 1000
        # essentially sets the accuracy of the failure rate for each
        # set of parameters. the pipe can get full if set too high.
        # try to catch failure if going above 500.

    # create the values to apply_async over
    # set how many threads to set for each value.
    for repeat in range(outer_loops):
        for codesize in [40]:
            for errtype in [4]:
                for strength in np.arange(0,1,0.1):
                    for variance in [1]:#np.arange(1, 15, 1):
                        for adjust in ['exactmanhat']: #pythag, manhat, gauss or leastweight
                            for pair in combined:
                                for expectedlength in [1]:#\
                                    #np.arange(0,8,0.5):
                                    # create an array of parameters, and then
                                    # apply all at once
                                    parameters.append([codesize,
                                                       expectedlength,
                                                       strength,
                                                       variance,
                                                       inner_loops,
                                                       errtype,
                                                       pair[0],
                                                       pair[1],
                                                       adjust])

    # create a dict to recombine all the data from loops
    # float and defaultdict together initialze missing key values to zero
    datadict = collections.defaultdict(float)

    maxq = 100  # determines how big the queue gets. tested to fail over 325.
    maxrange = int(len(parameters) / maxq + 1)
    counter = 0
    backup = open("backup.txt", 'w')
    # need to reduce total size, so queue doesnt get full.
    for subparams in [parameters[i * maxq:i * maxq + maxq]
                      for i in range(0, maxrange)]:
        #L, length, strength, variance, loops, errtype, CorrLen, anyons, adjust

        print(str(100.0 * counter / maxrange) + ' % done ')
        ###################################
        # set up the multiprocessing
        global errors
        global loopdata
        errors = mp.Queue(0)  # return errors
        loopdata = mp.Queue(0)  # stores each loops data

        #threadcount = mp.cpu_count() -1
        threadcount = 100  # len(parameters) #careful
        pool = mp.Pool(processes=threadcount)  # to create multiple processes
        for config in subparams:
            # apply multithreading
            processors = pool.apply_async(worker, config)
        pool.close()
        pool.join()

        # empty the queue
        while loopdata.qsize() != 0:
            got = loopdata.get()
            backup.write(str(got) + '\n')
            datadict[tuple(got[:6 + 1])] += 1.0 * \
                (got[7] + got[8]) / (2 * outer_loops)
        counter += 1
        while errors.qsize() != 0:  # error reporting
            print("EXCEPTION")
            print(str(errors.get()))

    ###################################

    # save the data
    filename = ('./CodePy2/data/highMT_l_' +
                str(int(outer_loops * inner_loops)) + '_' + uuid.uuid4().hex)
    data = open(filename + ".txt", 'w')
    print('L, w_bar, strength, sigma_sq, anyons, N, p_failure')
    data.write('L, w_bar, strength, sigma_sq, anyons, N, p_failure \n')
    for i in datadict:
        # print data
        print(str(i) + str(datadict[i]))
        # save to file
        for j in i:
            data.write(str(j) + ', ')
        data.write(str(datadict[i]) + '\n')

    print(str(datetime.datetime.now().isoformat()))
    funmath.toc()

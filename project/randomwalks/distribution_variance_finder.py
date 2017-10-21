"""calculates the variables for the gamma dist from
the walk data in manhat_pythag_data.txt
it then writes the gamma info for both the manhat and pythag
to the file gamma_info.txt"""

import funmath
import walks
import math
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import seaborn as sns
import random
from scipy.stats import gamma

import exactwalklengthcalculator as ex
file = open('gamma_info.txt','w')


loops = 1000000
N=32
rawdata = np.loadtxt('manhat_pythag_data.txt' ,  delimiter=',', skiprows=0, unpack=False)

pythag_data = rawdata[:,0]
manhat_data = rawdata[:,1]

pythag_var = np.var(pythag_data, dtype=np.float64)
manhat_var = np.var(manhat_data, dtype=np.float64)

#fit a gamma distribution
    #to the pythag data
pythag_fit_alpha, pythag_fit_loc, pythag_fit_beta = gamma.fit(pythag_data)
pythag_dist = gamma(pythag_fit_alpha, pythag_fit_loc, pythag_fit_beta )
    #to the manhat data
manhat_fit_alpha, manhat_fit_loc, manhat_fit_beta = gamma.fit(manhat_data)
manhat_dist = gamma(manhat_fit_alpha, manhat_fit_loc, manhat_fit_beta )
#save info

file.write(str(pythag_fit_alpha)+','+ str(pythag_fit_loc)+',' + str(pythag_fit_beta)+'\n')
file.write(str(manhat_fit_alpha)+','+ str(manhat_fit_loc)+',' + str(manhat_fit_beta)+'\n')

import numpy as np
p = 0.0031365  #value to calculate error for
n = 1600*40000 #number of loops
z = 1.96 #confidence interval
err = 1.0*z*np.sqrt((1.0/n)*p*(1.0-p))
print(err)

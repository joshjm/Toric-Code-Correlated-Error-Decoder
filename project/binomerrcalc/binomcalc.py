import numpy as np
p = 0.2  #value to calculate error for
n = 50000 #number of loops
z = 1.96 #confidence interval
err = 1.0*z*np.sqrt((1.0/n)*p*(1.0-p))
print(err)

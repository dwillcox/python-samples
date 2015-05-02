import numpy as np
from scipy.integrate import nquad

# Define function to integrate
def f(x,y,z):
    return np.exp(np.sin(x*x*np.pi/5.0)*np.cos(y*y*np.pi/5.0)*np.sin(z*z*np.pi/5.0))

integral = nquad(f,[[0,100.0],[0.0,100.0],[0.0,100.0]])
print 'Integral in region 100x100x100: ' + str(integral)




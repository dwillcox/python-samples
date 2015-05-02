"""
Integrate the function f(x,y,z) over the box with sides ranging over [0,100) using Monte Carlo.

Pass the number of points to use for Monte Carlo as a single integer command line parameter.
"""
import numpy as np
import sys

# Define function to integrate
def f(x,y,z):
    return np.exp(np.sin(x*x*np.pi/5.0)*np.cos(y*y*np.pi/5.0)*np.sin(z*z*np.pi/5.0))

# Define function to get a random 3D point in the box with sides [0,100]
def getp():
    return tuple(100.0*np.random.random(3))

try:
    N = int(sys.argv[1])
except:
    print 'Please enter a single integer command line argument specifying number of points.'
    exit()

# Integrate function
fave = 0.0
for i in xrange(N):
    pt = getp()
    fave += f(*pt)/N

# Write output
Volume = 100.0**3.0
integral = Volume*fave
print 'Integral in region 100x100x100: ' + str(integral)




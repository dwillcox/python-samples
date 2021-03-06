"""
Integrate the function f(x,y,z) over the box with sides ranging over [0,100) using Monte Carlo.

Pass the number of points to use for Monte Carlo as a single integer command line parameter.
"""
from mpi4py import MPI
import numpy as np
import sys

# Global MPI data structures
mpi_comm = MPI.COMM_WORLD # communicator object
mpi_size = mpi_comm.Get_size() # number of processors available
mpi_rank = mpi_comm.Get_rank() # which processor am I?

# Define function to integrate
def f(x,y,z):
    return np.exp(np.sin(x*x*np.pi/5.0)*np.cos(y*y*np.pi/5.0)*np.sin(z*z*np.pi/5.0))

# Define function to get a random 3D point in the box with sides [0,100]
def getp():
    return tuple(100.0*np.random.random(3))

# Number of points: pass as a command-line argument
if (mpi_rank == 0):
    try:
        N = int(sys.argv[1])
    except:
        print 'Please enter a single integer command line argument specifying number of points.'
        exit()
    # Get number of points per processor
    remainder = N%mpi_size
    ppp = (N-remainder)/mpi_size
    # Use ppp for the rest of the processors and ppp+remainder for the rank 0 processor
    if mpi_size > 1:
    	for i in xrange(1,mpi_size):
		# Send the ppp and N variables to the other processors, tagged for identification.
		mpi_comm.send(ppp,dest=i,tag=0)
		mpi_comm.send(N,dest=i,tag=2)
    # Set the value of ppp used by the rank 0 processor
    ppp += remainder

if mpi_rank != 0:
	# Only non-root processors should receive the ppp and N variables. 
	# Note the tag identifies the transaction and matches the ppp or N send commands above.
	ppp = mpi_comm.recv(source=0,tag=0)
	N = mpi_comm.recv(source=0,tag=2)

# Integrate function
fave = 0.0
for i in xrange(ppp):
    pt = getp()
    fave += f(*pt)/N
if mpi_rank != 0:
	# Send the results of each non-root processor back to root.
	mpi_comm.send(fave,dest=0,tag=1)

# Write output using root processor
if (mpi_rank == 0):
    Volume = 100.0**3.0
    for i in xrange(1,mpi_size):
	# The root processor retrieves the contributions from others
        fave += mpi_comm.recv(source=i,tag=1)
    integral = Volume*fave
    print 'Integral in region 100x100x100: ' + str(integral)




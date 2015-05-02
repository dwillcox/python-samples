import multiprocessing
import ctypes
import numpy as np
from functools import partial
from SharedMemory2Numpy import shared2np

# Some definitions
n = 10000
n_procs = 2
s2np = shared2np()
a = multiprocessing.Array(ctypes.c_double, n*n)
np_a = s2np.shmem_as_ndarray(a).reshape((n,n))
t_avg = multiprocessing.Array(ctypes.c_double, n)
np_t_avg = s2np.shmem_as_ndarray(a)

#print 'Shared memory array as a numpy array'
#print np_a

# Do some parallel processing
# Note how I'm passing parameters to the functions, since pool.map can pass only 1 argument.
# For reference, using functools.partial doesn't help either (see comments below).
def filla(i, nj=n, p=np_a):
    p[i][:] = np.fromfunction(lambda k,j: np.exp(np.sin(i*np.pi/5.0)*np.cos(j*np.pi/5.0)),(1,nj),dtype=np.float64)
    #p[i][:] = np.fromfunction(lambda k,j: (i+1)*(j+1),(1,nj),dtype=np.float64)

pool = multiprocessing.Pool(processes=n_procs)
pool.map(filla, range(n))
pool.close()
pool.join()

#print 'Filled shared memory numpy array:'
#print np_a

# get the average of the array
#avg = np.average(np_a)
#print 'Average: ' + str(avg)
def rowaverage(i,t_avg=np_t_avg,p=np_a):
    np_t_avg[i] = np.mean(p[i])

pool = multiprocessing.Pool(processes=n_procs)
pool.map(rowaverage,range(n))
pool.close()
pool.join()
avg = np.mean(np_t_avg)

def avgmask(i,ave=avg,p=np_a):
    meanrow = np.average(p[i])
    # Assign values from rows not 'belonging' to this process
    if meanrow < ave:
#	print 'Below average, i=' + str(i)
        if i == len(p)-1:
	# Replace the last row's contents  with those of the first row.
            p[i][:] = p[0][:]
        else:
	# Replace row i with the contents of row i+1
            p[i][:] = p[i+1][:]

# Note that passing parameters using functools.partial isn't compatible with pool.map for some reason
#avpart = partial(avgmask,ave=avg,p=np_a)

pool = multiprocessing.Pool(processes=n_procs)
# See Note above: functools.partial not compatible.
#pool.map(avpart,range(n))
pool.map(avgmask,range(n))
pool.close()
pool.join()
#print 'Rows in shared array with below-average averages replaced by subsequent rows.'
#print np_a

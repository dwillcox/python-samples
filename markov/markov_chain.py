# Create a simple Markov chain and do some timing
import numpy as np
import profile

t = profile.timer('python markov')
t.begin()
m = np.array([[0.1, 0.2, 0.3],
              [0.7, 0.2, 0.5],
              [0.2, 0.6, 0.2]],dtype=np.float64)

xini = np.array([[1, 0, 0]],dtype=np.float64)

nstate = len(xini.flat)
N = 1000000
mx = np.zeros((nstate,N),dtype=np.float64)

mx[:,0] = xini
for i in xrange(1,N):
    mx[:,i] = np.dot(m,mx[:,i-1])

ave = np.mean(mx[:,1:],axis=1)
std = np.std(mx[:,1:],axis=1)

t.end()

#print mx
print 'Iterations: ' + str(N)
print 'Initial State: '
print xini
print 'Average State: '
print ave
print 'State Standard Deviation: '
print std
profile.timeReport()


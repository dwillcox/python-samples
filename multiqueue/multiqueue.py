from mpi4py import MPI
import sys
import shlex
import subprocess
from collections import OrderedDict

"""
This program should be run using mpiexec with one command-line argument
specifying the name of the job file to use.

Lines in the job file are either comments (line begins with '#') or 
they are shell commands to execute, one shell command per line.

multiqueue.py will execute one command in the job file per thread available.
If there are more threads (N_THREADS) than job commands (N_JOBS), then
only N_JOBS threads will be used. If there are more job commands than threads, only the first N_THREADS jobs will be run.
"""


# Global MPI information
mpi_comm = MPI.COMM_WORLD
mpi_size = mpi_comm.Get_size()
mpi_rank = mpi_comm.Get_rank()

def startjob(job):
	# Use subprocess.call to start job on this thread
	subprocess.Popen(shlex.split(job))

# Master: Read parameter file and get jobs
if (mpi_rank == 0):
	av = sys.argv
	lav = len(av)
	pname = 'multiqueue.par'
	if lav==2:
		pname = av[1]
	elif lav>2:
		print 'Error: more than 1 command line arguments.'
		mpi_comm.Abort()

	try:
		fpar = open(pname,'r')
	except IOError:
		print 'Error: could not open parameter file - ' + pname
		mpi_comm.Abort()
		
	jobs = []
	for l in fpar:
		# Ignore commented lines (that start with '#')
		l=l.strip()
		if l=='':
			continue
		elif l[0]!='#':		
			jobs.append(l.strip())
	fpar.close()
	
	njobs = len(jobs)
	for m in xrange(1,mpi_size):
		# tag 0 is njobs
		mpi_comm.send(njobs,dest=m,tag=0)

	jmax = min((njobs,mpi_size))
	for j in xrange(1,jmax):
		# tag 1 is the job
		mpi_comm.send(jobs[j],dest=j,tag=1)
	
	# Now start job 0 on Master
	startjob(jobs[0])

else:
	# Get njobs from Master
	njobs = mpi_comm.recv(source=0,tag=0)
	
	# Get a job if there is one for this thread
	if mpi_rank < njobs:
		myjob = mpi_comm.recv(source=0,tag=1)
		# start job 
		startjob(myjob)	

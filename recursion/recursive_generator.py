import itertools as it
import profile # Mike Zingale's profile module from http://bender.astro.sunysb.edu/classes/python-science/lectures/profile.py

def permx(x,y=None,ntot=None):
        """
        This generator is an iterable which returns unique 
        permutations picking 1 element from each of the lists
        in x. It is equivalent to for loops nested at 
        depth len(x) such that the top level loop scans 
        over the elements of x[0] and the deepest level loop 
        scans the elements of x[-1].

        When calling permx, pass one argument into x: a list of lists.
        The arguments y and ntot permit permx to call 
        itself and remember the list y containing the current permutation
        and the integer ntot which is the length of list x.
        """
        if y==None:
                y = ['' for xi in x] # Construct a list of length len(x)
        if ntot==None:
                ntot = len(x) # Remember the length of the top-level list x
        
        # pos is 0 at the top level and increments with each level of recursion
        # so it's also the index in y at this instance of permx
        pos = ntot-len(x) 
        
        for xi in x[0]:
                # Selects elements from the first entry x[0] in the list x
                # which could be either the top-level list as the user
                # passed to permx or part of it if the current 
                # call to permx was recursive.
                y[pos] = xi
                if (pos==ntot-1):
                        # The current call to permx is iterating over 
                        # the final element of the top-level list x 
                        # so we're done constructing the permutation list
                        # and can yield it back to either the user (if ntot==1)
                        # or pass it back up the recursion levels.
                        yield y
                else:
                        # Iterate over the remaining elements of x
                        for p in permx(x[1:],y,ntot):
                                # Since we just passed the same list y 
                                # through all recursive calls to permx,
                                # it now contains elements from every 
                                # list x[i] in the top-level list x.
                                # This passes y back up the recursion levels
                                # until it reaches the top and is passed back
                                # to the user (if ntot>1)
				yield y

xtest = [['a','b','c'],[0,1],[3.0,4.0]]

print 'Using the recursive generator: '
t1 = profile.timer('recursive generator')
t1.begin()
for p in permx(xtest):
	print p
t1.end()

print '-------------------------------'
print 'Using itertools.product: '
t2 = profile.timer('itertools.product')
t2.begin()
for p in it.product(*xtest):
        print p
t2.end()

profile.timeReport()

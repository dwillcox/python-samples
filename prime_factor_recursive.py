def pfactor(n,flist=None):
    if flist==None:
        flist=[]
    if n==2:
        flist.append(2)
        return flist
    for i in xrange(2,n):
        if (n%i==0):
            flist.append(i)
            flist = pfactor(n//i,flist)
            return flist
    flist.append(n)
    return flist

def user():
    print '-----------------------------------------------'
    print 'Please enter a number you would like to factor.'
    print 'Enter any character string to quit. '
    s = raw_input('>')
    try:
        print 'Prime Factors: ' + str(pfactor(int(s)))
        user()
    except ValueError:
        print 'Exiting...'
        exit()

user()

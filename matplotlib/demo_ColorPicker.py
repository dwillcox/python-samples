from ColorPicker import ColorPicker
import matplotlib.pyplot as plt
import numpy as np
import sys

# Get the number of colors from one command line integer argument
try:
	Nh = int(sys.argv[1])
	Ns = int(sys.argv[2])
	Nv = int(sys.argv[3])
	N = Nh*Ns*Nv
except:
	print 'Please enter three command line integers specifying the number of colors to generate in hsv.'
	exit()

# Now get the colors
cpick = ColorPicker()
print 'hsv: ' + str(Nh) + ',' + str(Ns) + ',' + str(Nv)
colors = cpick.pickColors(Nh,Ns,Nv)
print colors
# Generate sample data
class Line:
	def __init__(self,x,a,b):
		self.x = np.array(x)
		self.y = a*self.x+b
			
intercept = 0.0
npts = 10
xvector = np.linspace(0,1.0,npts,dtype=np.float64)
data = []
for i in xrange(N):
	data.append(Line(xvector,float(i+1),intercept))

# Now make a sample plot!
plt.figure(1)
fig = plt.gcf()
ax1 = fig.add_axes([0.1,0.1,0.8,0.8])
ax1.axes.get_xaxis().set_visible(False)
ax1.axes.get_yaxis().set_visible(False)
for i in xrange(N):
	ax1.plot(data[i].x,data[i].y,color=colors[i],linestyle='-')
plt.title('Number of Divisions in (H,S,V): (' + str(Nh) + ',' + str(Ns) + ',' +
	str(Nv) + ')')
plt.show()	


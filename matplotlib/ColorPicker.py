import math
import numpy as np
import itertools

class ColorPicker:
	def __init__(self):
		self.hsv = []
		self.rgb = []

	def hsv2rgb(self,hsv):
		h = hsv[0]
		s = hsv[1]
		v = hsv[2]
		c = v*s
		hp = h/60.0
		x = c*(1-abs((hp%2) - 1))
		m = v-c
		rgb = [0,0,0]
		if (0 <= hp < 1):
			rgb = [c,x,0]
		elif (1 <= hp < 2):
			rgb = [x,c,0]
		elif (2 <= hp < 3):
			rgb = [0,c,x]
		elif (3 <= hp < 4):
			rgb = [0,x,c]
		elif (4 <= hp < 5):
			rgb = [x,0,c]
		elif (5 <= hp < 6):
			rgb = [c,0,x]
		return rgb
	
	def subdivide_hsv(self,nh,ns,nv):
		# Return a list of hsv lists [h,s,v] evenly chosen from domain
		h_max = 360.0
		s_max = 1.0
		v_max = 1.0
		
		# get lists of hsv values possible, removing first and last
		h = np.linspace(0.0,h_max,nh,endpoint=False)
		s = np.linspace(0.0,s_max,ns+1,endpoint=True)[1:]
		v = np.linspace(0.0,v_max,nv+1,endpoint=True)[1:]
		
		# combine hsv using cartesian product of h, s, v
		self.hsv = [hsvi for hsvi in itertools.product(h,s,v)]
		return self.hsv

	def pickColors(self,nh,ns,nv):
		self.subdivide_hsv(nh,ns,nv)
		self.rgb = []
		for hsvi in self.hsv:
			self.rgb.append(tuple(self.hsv2rgb(hsvi)))
		return self.rgb

		

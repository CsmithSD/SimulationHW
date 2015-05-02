##############################################################################
# Problem: 7.21, "Fundamentals of Natural Computing"
# Author: Stephanie Athow
# Date: 18 April 2015
# Problem Statement:
#	Implement the random midpoint displacement algorithm in 3D and generate
#	some fractal landscapes. Study the influence of H on the landscapes 
#	generated.
###############################################################################

import numpy as np
import random
import scipy 
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.interpolate import griddata

NRC = 5			# number of recursion calls
sigma = 12		# standard deviation of the Gaussian distribution
mu = 5			# mean of Gaussian distribution
H = 0.75		# should be 0 < H < 1

###############################################################################
#								Recursion
#	Recursively applies subdivision of the grid
###############################################################################
def Recursion( grid, delta, x0, x2, y0, y2, t, nrc ):
	x1 = ( x0 + x2 ) / 2
	y1 = ( y0 + y2 ) / 2

	neighbors = grid[x0][y0] + grid[x0][y2] + grid[x2][y0] + grid[x2][y2]
	val = 0.25 * neighbors + delta[t] * random.gauss( mu, sigma )
	grid[x1][y1] = val
	
	if (t < nrc):
		Recursion( grid, delta, x0, x1, y0, y1, t+1, nrc )
		Recursion( grid, delta, x0, x1, y1, y2, t+1, nrc )
		Recursion( grid, delta, x1, x2, y1, y2, t+1, nrc )
		Recursion( grid, delta, x1, x2, y0, y1, t+1, nrc )

###############################################################################
#								Plot
###############################################################################
def plotImage( grid, delta, NRC, N ):
	X = []
	Y = []
	Z = []
	fig = plt.figure()
	ax = fig.add_subplot( 111, projection = '3d' )
	numrows = len( grid )
	numcols = len( grid[0] )

	for i in range( 0, numrows ):
		for j in range( 0, numcols ):
			x, y = i, j
			height = grid[i][j]
			X.append(x)
			Y.append(y)
			Z.append(height)
	
	ax.plot_trisurf( X, Y, Z)
	
	#plt.grid( True )
	plt.show()
	plt.savefig( 'brownian_surface.png' )

###############################################################################
#									Main
###############################################################################
random.seed()									
N = pow( 2, NRC )								# number of points
grid = np.zeros( (N-1, N-1), dtype=float )		# holds grid
grid[ N-2, N-2 ] = sigma*random.gauss( mu, sigma )	# end point
delta = np.zeros( ( N-1, 1 ), dtype=float )			# holds variances 

for i in range(0, NRC-1):
	delta[i] = sigma * pow( 0.5, (i+1)/2 )
	
Recursion( grid, delta, 0, N-2, 0, N-2, 0, NRC-1 )

plotImage( grid, delta, NRC, N )
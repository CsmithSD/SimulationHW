# Author: Stephanie Athow
# Date: 21 April 2015
# Problem:
# 	Modify the heat flow example to deal with insulated conditions on the top
#	and bottom boundary. Insulation means zero flux or:
# 		u[N][j] = u[N-1][j]
# 	This implies that instead of a fixed valued ghost points on the top and
# 	bottom, you modify the CA rule using the previous relation.

import numpy as np
import matplotlib.pyplot as plt

N = 100				# grid size (square)
time_end = 1500		# time step end	

t_source = 10
t_grid = np.zeros( [N, N] ) 	# holds grid of temps
t_update = np.zeros( [N, N] )	# holds update values

# initialize heat source
for i in range( 0, N ):
	t_grid[i][N-1] = i*( N-1-i )

# run CA on grid for time_end loops
for i in range( 1, time_end ):

	# update top/bottom boundaries
	for k in range( 0, N ):
		t_update[0][k] = t_grid[1][k]
	for k in range( 0, N ):
		t_update[N-1][k] = t_grid[N-2][k]

	# update inside cells
	# loop rows
	for j in range( 1, N-1 ):
		# loop columns
		for k in range( 1, N ):
			if( k == N-1 ):
				t_update[j][k] = t_grid[j][k]

			else:
				neighbors = t_grid[j-1][k] + t_grid[j+1][k] + t_grid[j][k-1] + t_grid[j][k+1]
				update_temp = neighbors / 4.0
				t_update[j][k] = update_temp

	
	# time update t_grid
	#del t_grid
	t_grid = t_update
	
fig, ax = plt.subplots()
ax.imshow( t_grid, cmap=plt.cm.gray, interpolation='nearest' )

plt.show()
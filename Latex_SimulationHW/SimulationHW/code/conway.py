import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation


cells = 100
alive = 255
dead = 0
vals = [alive, dead]
grid = np.random.choice(vals, cells*cells, p=[0.1, 0.9]).reshape(cells, cells)

def update(*args):
    global grid
    next_grid = grid.copy()
    for i in range(cells):
        for j in range( cells):
            count = ( grid[ i, ( j-1 ) % cells  ] + 
                      grid[ i, ( j+1 ) % cells  ] + 
                      grid[( i - 1 ) % cells, j ] + 
                      grid[( i + 1 ) % cells, j ] + 
                      grid[( i - 1 ) % cells, ( j - 1 ) % cells ] + 
                      grid[( i - 1 ) % cells, ( j + 1 ) % cells ] +
                      grid[( i + 1 ) % cells, ( j - 1 ) % cells ] + 
                      grid[( i + 1 ) % cells, ( j + 1 ) % cells ] ) / 255
            if grid[ i, j ] == alive:
                if( count < 2 or count > 3):
                    next_grid[i, j] = dead
            else:
                if count == 3:
                    next_grid[i, j] = alive
    mat.set_data(next_grid)
    grid = next_grid
    return [mat]

fig, ax = plt.subplots()
mat = ax.matshow(grid)
ani = animation.FuncAnimation(fig, update, interval = 100 )
plt.show()

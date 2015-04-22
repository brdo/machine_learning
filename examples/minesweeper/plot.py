
import time
import math
import numpy as np
import matplotlib.pyplot as plt

def init_plot(width, height):
    plt.axis([0, width, 0, height])
    plt.ion()
    plt.show()

def redraw_plot(mines, tanks, delay=0.05):

    cmap = plt.get_cmap('hsv')
    points = []
    for mine in mines:
        pnt = plt.scatter(mine.position.x, mine.position.y,
                          cmap = cmap, color = [0,0,1],
                          linewidths = 10, marker = 'x', alpha = 0.5)
        points.append(pnt)

    max_fitness = max([t.fitness for t in tanks])

    for t, tank in enumerate(tanks):
        tank.update(mines)
        rotation = 180 / ( math.pi ) * math.atan(tank.bearing.y/tank.bearing.x)
        pnt = plt.scatter(tank.position.x, tank.position.y,
                          cmap = cmap,
                          color = [float(tank.fitness)/max_fitness,0,0]\
                                   if max_fitness else [0,0,0],
                          linewidths = 10,
                          marker = (4, 0, rotation))
        points.append(pnt)

    plt.draw()

    time.sleep(delay)

    for pnt in points:
        pnt.remove()

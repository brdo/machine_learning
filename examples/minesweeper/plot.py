
import time
import numpy as np
import matplotlib.pyplot as plt

def init_plot(width, height):
    plt.axis([0, width, 0, height])
    plt.ion()
    plt.show()

def redraw_plot(mines, tanks, delay=0.05):

    points = []
    for mine in mines:
        pnt = plt.scatter(mine.position.x, mine.position.y, linewidths = 10, alpha = 0.1)
        points.append(pnt)

    max_fitness = max([t.fitness for t in tanks])

    for tank in tanks:
        tank.update(mines)
        pnt = plt.scatter(tank.position.x, tank.position.y, linewidths = 10, marker = '^')
        points.append(pnt)

    plt.draw()

    time.sleep(delay)

    for pnt in points:
        pnt.remove()

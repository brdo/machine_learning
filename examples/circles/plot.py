
import time
import math
import numpy as np
import matplotlib.pyplot as plt

def init_plot(width, height):
    """
    initialize the plot
    """
    axes = plt.axis([0, width, 0, height])
    plt.ion()
    plt.axes().set_aspect('equal')
    plt.show()

def redraw_plot(obstacles, disks, delay=0.05):
    """
    redraw the plot
    """

    cmap = plt.get_cmap('hsv')
    fig = plt.gcf().gca()

    for obstacle in obstacles:
        circle = plt.Circle((obstacle.position.x, obstacle.position.y),
                            obstacle.radius)

        fig.add_artist(circle)

    disks = sorted(disks, key=lambda d: d.fitness, reverse=True)

    max_fitness = max([t.fitness for t in disks])

    circles = []
    # plot the top 5 disks
    for disk in disks[0:5]:
        if disk.fitness > 0:

            # print the most fit disk
            if disk.fitness == max_fitness:
                print disk

            circle = plt.Circle((disk.position.x, disk.position.y),
                                disk.radius, color=[1,0,0],
                                alpha = 1 if disk.fitness == max_fitness else 0.1)

            fig.add_artist(circle)
            circles.append(circle)

    plt.draw()
    plt.pause(0.001)

    for circle in circles:
        circle.remove()


import time
import math
import numpy as np
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import matplotlib.text as txt

def init_plot(width, height):
    """
    initialize the plot
    """
    plt.axis([0, width, 0, height])
    plt.ion()
    plt.axes().set_aspect('equal')
    plt.show()

def redraw_plot(beams, planes, delay=0.05):
    """
    redraw the plot
    """

    cmap = plt.get_cmap('hsv')
    points = []
    fig = plt.gcf().gca()

    max_load= max([b.load for b in beams]) or 1
    for b, beam in enumerate(beams):
        beam.color = cm.jet(b*1.0/len(beams))
        text = plt.text(beam.position.x, beam.position.y, str(int(beam.load*100)))
        circle = plt.Circle((beam.position.x, beam.position.y),
                            beam.radius, fill=False,
                            color = beam.color,
                            )

        points.append(circle)
        points.append(text)
        fig.add_artist(circle)

    max_fitness = max([t.fitness for t in planes])

    for t, plane in enumerate(planes):
        rotation = 180 / ( math.pi ) * math.atan(plane.bearing.y/plane.bearing.x)
        pnt = plt.scatter(plane.position.x, plane.position.y,
                          cmap = 'jet',
                          color = plane.beam.color if plane.beam else [0.5, 0.5, 0.5],
                          linewidths = 10,
                          marker = (2, 0, rotation))
        points.append(pnt)

    plt.draw()
    plt.pause(0.001)

    for pnt in points:
        pnt.remove()

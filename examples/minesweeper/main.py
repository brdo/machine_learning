#!/usr/bin/python

import time

from minesweep import *
from genalg import Algorithm
from plot import init_plot, redraw_plot

mines = generate_mines(50)
tanks = generate_tanks(40)

alg = Algorithm(len(tanks),
                len(tanks[0].neural_net.get_weights()))
init_plot(WIDTH, HEIGHT)

t = 0
while True:

    if t == 0:
        for c, chromosome in enumerate(alg.chromosomes):
            tanks[c].neural_net.set_weights(chromosome.weights)
            tanks[c].fitness = 0
            print c, tanks[c], tanks[c].neural_net.get_weights()[0]
            #print tanks[c].neural_net

    if t < 150:
        for i, tank in enumerate(tanks):
            closest_mine = tank.update(mines)
            vec = Vector(closest_mine.position.x, closest_mine.position.y)
            distance = vec.distance(tank.position)
            if 2 > distance:
                tank.fitness += 10
                closest_mine.relocate()
            alg.chromosomes[i].fitness = tank.fitness
        redraw_plot(mines, tanks)
        t += 1

    else:
        t = 0
        alg.epoch()
        print 'generation', alg.generation


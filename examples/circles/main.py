#!/usr/bin/python

import time

from circles import *
from genalg import Algorithm
from plot import init_plot, redraw_plot

obstacles = generate_obstacles(10)
disks = generate_disks(1000)

alg = Algorithm(len(disks), 3)
init_plot(WIDTH, HEIGHT)

while True:

    for c, chromosome in enumerate(alg.chromosomes):
        disks[c].set_chromosome(chromosome)

    for i, disk in enumerate(disks):
        disk.update(obstacles)
        alg.chromosomes[i].fitness = disk.fitness

    redraw_plot(obstacles, disks)

    alg.epoch()
    print 'generation', alg.generation

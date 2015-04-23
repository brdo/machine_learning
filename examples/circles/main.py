#!/usr/bin/python

import time

from circles import *
from genalg import Algorithm
from plot import init_plot, redraw_plot

CROSSOVER_RATE = 0.7
MUTATION_RATE = 0.1
POP_SIZE = 1000
MAX_GENERATIONS = 200
NUM_OBSTACLES = 10

def main():
    """
    run the program
    """

    from optparse import OptionParser

    parser = OptionParser()

    parser.add_option("--num-obstacles", type='int',
                      dest="num_obstacles", default=NUM_OBSTACLES,
                      help="number of obstacles")

    parser.add_option("--pop-size", type='int',
                      dest="pop_size", default=POP_SIZE,
                      help="population size")

    parser.add_option("--crossover-rate", type='float',
                      dest="crossover_rate", default=CROSSOVER_RATE,
                      help="crossover rate")

    parser.add_option("--mutation-rate", type='float',
                      dest="mutation_rate", default=MUTATION_RATE,
                      help="mutation rate")

    parser.add_option("--max-generations", type='int',
                      dest="max_generations", default=MAX_GENERATIONS,
                      help="maximum nubmer of generations")

    options, args = parser.parse_args()

    obstacles = generate_obstacles(options.num_obstacles)
    disks = generate_disks(options.pop_size)

    chromo_length = 3 # x, y, r
    alg = Algorithm(chromo_length,
                    options.pop_size, options.crossover_rate,
                    options.mutation_rate)
    init_plot(WIDTH, HEIGHT)

    while alg.generation < options.max_generations:

        for c, chromosome in enumerate(alg.chromosomes):
            disks[c].set_chromosome(chromosome)

        for i, disk in enumerate(disks):
            disk.update(obstacles)
            alg.chromosomes[i].fitness = disk.fitness

        redraw_plot(obstacles, disks)

        alg.epoch()
        print 'generation', alg.generation

if __name__ == '__main__':
    main()

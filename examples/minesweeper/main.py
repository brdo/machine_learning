#!/usr/bin/python

import time

from minesweep import *
from genalg import Algorithm
from plot import init_plot, redraw_plot

CROSSOVER_RATE = 0.7
MUTATION_RATE = 0.1
POP_SIZE = 40
MAX_GENERATIONS = 200
NUM_MINES = 50

def main():
    """
    run the program
    """

    from optparse import OptionParser

    parser = OptionParser()

    parser.add_option("--num-mines", type='int',
                      dest="num_mines", default=NUM_MINES,
                      help="number of mines")

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

    mines = generate_mines(options.num_mines)
    tanks = generate_tanks(options.pop_size)

    alg = Algorithm(len(tanks[0].neural_net.get_weights()),
                    options.pop_size, options.crossover_rate,
                    options.mutation_rate)

    init_plot(WIDTH, HEIGHT)

    t = 0
    while alg.generation < options.max_generations:

        if t == 0:
            for c, chromosome in enumerate(alg.chromosomes):
                tanks[c].neural_net.set_weights(chromosome.weights)
                tanks[c].fitness = 0
                print c, tanks[c]

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

if __name__ == '__main__':
    main()

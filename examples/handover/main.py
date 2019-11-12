#!/usr/bin/python

import time

from handover import *
from genalg import Algorithm
from plot import init_plot, redraw_plot

CROSSOVER_RATE = 0.7
MUTATION_RATE = 0.1
POP_SIZE = 40
MAX_GENERATIONS = 200
NUM_BEAMS = 3

def main():
    """
    run the program
    """

    from optparse import OptionParser

    parser = OptionParser()

    parser.add_option("--num-beams", type='int',
                      dest="num_beams", default=NUM_BEAMS,
                      help="number of beams")

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

    beams = generate_beams(options.num_beams)
    planes = generate_planes(options.pop_size)

    alg = Algorithm(len(planes[0].neural_net.get_weights()),
                    options.pop_size, options.crossover_rate,
                    options.mutation_rate)

    init_plot(WIDTH, HEIGHT)

    def describe():
        fitness = 0
        action = 0
        for i, plane in enumerate(planes):
            fitness += plane.fitness
            action += plane.action
        print t, 'FITNESS', fitness/len(planes)
        print t, 'ACTION', action/len(planes)

    def reset():
        for b in beams:
            b.reset()

        for p in planes:
            p.reset()

    def animate():
        # ----
        chromosome = sorted(alg.chromosomes, key=lambda x: x.fitness, reverse=True)[0]

        for i, plane in enumerate(planes):
            plane.neural_net.set_weights(chromosome.weights)

        for _ in range(150):
            for i, plane in enumerate(planes):
                beam = plane.update(beams)
            redraw_plot(beams, planes)

        reset()


    t = 0
    while alg.generation < options.max_generations:

        if t == 0:
            print len(alg.chromosomes)
            for c, chromosome in enumerate(alg.chromosomes):
                planes[c].neural_net.set_weights(chromosome.weights)
                planes[c].reset()
                print c, planes[c]

        if t < 300:
            for i, plane in enumerate(planes):
                beam = plane.update(beams)
                alg.chromosomes[i].fitness = plane.fitness
            # describe()
#           redraw_plot(beams, planes)
            t += 1

        else:
            t = 0
            reset()
            alg.epoch()
            print 'generation', alg.generation

            if alg.generation % 10 == 0:
                animate()
if __name__ == '__main__':
    main()

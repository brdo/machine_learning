
import time

from minesweep import *
from genalg import Algorithm
from plot import init_plot, redraw_plot

mines = generate_mines(40)
tanks = generate_tanks(20)

alg = Algorithm(len(tanks),
                len(tanks[0].neural_net.get_weights()))
init_plot(WIDTH, HEIGHT)

t = 0
while True:

    if t == 0:
        for c, chromosome in enumerate(alg.chromosomes):
            tanks[c].neural_net.set_weights(chromosome.weights)
            print tanks[c]

    if t < 50:
        for i, tank in enumerate(tanks):
            closest_mine = tank.update(mines)
            vec = Vector(closest_mine.position.x, closest_mine.position.y)
            distance = vec.distance(tank.position)
            if 7 > distance:
                tank.fitness += 1
                alg.chromosomes[i].fitness = tank.fitness
                print 'score', tank
                closest_mine.relocate()
            elif 2 > distance:
                tank.fitness -= 1
                alg.chromosomes[i].fitness = tank.fitness

        redraw_plot(mines, tanks)
        t += 1

    else:
        t = 0
        alg.epoch()
        print 'generation', alg.generation



from utils import random_clamped
import random

CROSSOVER_RATE = 0.6
MUTATION_RATE = 0.05
MAX_PERTUBATION = 0.1

class Chromosome(object):
    def __init__(self, weights):
        self.fitness = 0
        self.weights = weights

    def mutate(self):
        for w in range(len(self.weights)):
            if random.random() < MUTATION_RATE:
                self.weights[w] += random_clamped() * MAX_PERTUBATION

    def __repr__(self):
        return 'Chromo(fitness=%5.2f)' %( self.fitness )

class Algorithm(object):
    def __init__(self, n_chromosomes, n_weights):
        self.generation = 1
        self.size = n_chromosomes

        self.chromosomes = []
        for _ in range(self.size):
            weights = [random_clamped() for _ in range(n_weights)]
            self.chromosomes.append(Chromosome(weights))

    def roulette(self):
        total_fitness = sum([c.fitness for c in self.chromosomes])
        rand_value = random.random() * total_fitness

        value = 0
        for c in self.chromosomes:
            value += c.fitness
            if value >= rand_value:
                return c

    def crossover(self, papa, mama):
        if random.random() > CROSSOVER_RATE:
            # no baby
            return papa, mama

        x = random.randint(0,len(papa.weights)-1)

        baby1 = Chromosome(papa.weights[0:x] + mama.weights[x:])
        baby2 = Chromosome(mama.weights[0:x] + papa.weights[x:])
        return baby1, baby2

    def epoch(self):

        chromosomes = sorted( self.chromosomes, key = lambda c: c.fitness, reverse = True )

        # breed
        new_chromosomes = []
        while len(new_chromosomes) < self.size:
            papa = self.roulette()
            mama = self.roulette()
            if papa and mama:
                baby1, baby2 = self.crossover(papa, mama)
                baby1.mutate()
                baby2.mutate()
                new_chromosomes.append(baby1)
                new_chromosomes.append(baby2)

        self.chromosomes = new_chromosomes
        self.generation += 1

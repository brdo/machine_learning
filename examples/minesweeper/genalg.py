
from utils import random_clamped
import random

class Chromosome(object):
    """
    Chromosome class
    """
    def __init__(self, weights, mutation_rate):
        self.weights = weights
        self.mutation_rate = mutation_rate

        self.fitness = 0

    def mutate(self, max_pertubation = 0.05):
        """
        mutate chromosome
        """
        for w in range(len(self.weights)):
            if random.random() < self.mutation_rate:
                self.weights[w] += random_clamped() * max_pertubation

    def __repr__(self):
        return 'Chromo(fitness=%5.2f)' %( self.fitness )

class Algorithm(object):
    """
    Genetic Algorithm class
    """
    def __init__(self, chromo_length, pop_size,
                 crossover_rate, mutation_rate):

        self.chromo_length = chromo_length
        self.pop_size = pop_size
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.generation = 1
        self.size = pop_size

        self.chromosomes = []
        for _ in range(self.size):
            weights = [random_clamped() for _ in range(chromo_length)]
            self.chromosomes.append(Chromosome(weights, mutation_rate))

    def roulette(self):
        """
        choose a chromosome at random but favor ones with higher fitness
        """
        total_fitness = sum([c.fitness for c in self.chromosomes])
        rand_value = random.random() * total_fitness

        value = 0
        for c in self.chromosomes:
            value += c.fitness
            if value >= rand_value:
                return c

    def crossover(self, papa, mama):
        """
        breed two chromosomes, return two new chromosomes
        """
        if random.random() > self.crossover_rate:
            # no baby
            return papa, mama

        x = random.randint(0,len(papa.weights)-1)

        baby1 = Chromosome(papa.weights[0:x] + mama.weights[x:], self.mutation_rate)
        baby2 = Chromosome(mama.weights[0:x] + papa.weights[x:], self.mutation_rate)
        return baby1, baby2

    def epoch(self):
        """
        run a single generation
        """
        chromosomes = sorted( self.chromosomes, key = lambda c: c.fitness, reverse = True )

        # breed
        new_chromosomes = []
        while len(new_chromosomes) < self.size:
            papa = self.roulette()
            mama = self.roulette()
            if papa and mama:
                baby1, baby2 = self.crossover(papa, mama)

                # mutate based on a cooling factor
                baby1.mutate(1.0/self.generation)
                baby2.mutate(1.0/self.generation)

                new_chromosomes.append(baby1)
                new_chromosomes.append(baby2)

        self.chromosomes = new_chromosomes
        self.generation += 1

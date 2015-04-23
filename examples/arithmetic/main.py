#!/usr/bin/python

"""
Genetic Algorithm Example: See http://www.ai-junkie.com/ga/intro/gat3.html

Overview:
Given the digits 0 through 9 and the operators +, -, * and /,
find a sequence that will output a given target number.

Equations are encoded using this translation
     0000 : 0
     0001 : 1
     0010 : 2
     0011 : 3
     0100 : 4
     0101 : 5
     0110 : 6
     0111 : 7
     1000 : 8
     1001 : 9
     1010 : +
     1011 : -
     1100 : *
     1101 : /

For example this equation would be sufficient for the target number 19

    5*4-3+2/1

encoding this becomes

    0101 1100 0100 1011 0011 1010 0010 1101 0001

which is the chromosome form of the equation

Equations must be of the form digit, operator, digit, ...
Some error handling is required to correct equations since random
mutations and recombination will break our format

    5*/44-+2 would reduce to 5*4-2

"""

import re
import random
import math

CHROMO_LEN = 500
CROSSOVER_RATE = 0.7
MUTATION_RATE = 0.001
POP_SIZE = 200
MAX_GENERATIONS = 1200


OPERATORS = '+-*/'
WINNER = 99
SYMBOLS = {
    '0000': '0',
    '0001': '1',
    '0010': '2',
    '0011': '3',
    '0100': '4',
    '0101': '5',
    '0110': '6',
    '0111': '7',
    '1000': '8',
    '1001': '9',
    '1010': '+',
    '1011': '-',
    '1100': '*',
    '1101': '/',
}

class Chromosome(object):
    """
    Chromosome class
    """
    def __init__(self, bits, mutation_rate):
        self.bits = bits
        self.mutation_rate = mutation_rate
        self.fitness = 0

    def valid(self):
        """
        test if chromosome has a valid expression
        """
        try:
            return None != self.value()
        except:
            return False

    def decode(self):
        """
        decode the bits into an equation digit, operator, digit, ...
        """
        expression = []
        for b in re.findall(r'....', self.bits):
            c = SYMBOLS.get(b,'?')
            if expression:
                if c.isdigit() and str(expression[-1]) in OPERATORS:
                    expression.append(int(c))
                elif c in OPERATORS and isinstance(expression[-1], int):
                    expression.append(c)
            elif c.isdigit():
                expression.append(int(c))

        if expression and not isinstance(expression[-1], int):
            expression = []

        expression = ''.join([str(c) for c in expression])
        return expression

    def value(self):
        """
        evaluate the expression
        """
        expression = self.decode()
        return eval(expression) if expression else None

    def mutate(self):
        """
        attempt to mutate each bit according to the mutation rate
        """
        for x in range(len(self.bits)):
            if random.random() < self.mutation_rate:
                b = int(self.bits[x])
                self.bits = self.bits[0:x] + str(0 if b else 1) + self.bits[x+1:]

    def __repr__(self):
        return 'Chromo(value=%10s, expr=%50s, fitness=%5.7f)'\
            %(self.value() if self.valid() else 'NaN', self.decode(),
              self.fitness)



class Algorithm(object):
    """
    Genetic Algorithm class
    """
    def __init__(self, value, chromo_length, pop_size,
                 crossover_rate, mutation_rate):

        self.value = value
        self.chromo_length = chromo_length
        self.pop_size = pop_size
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate

        self.generation = 0

        bits = ''.join([str(random.randint(0,1)) for _ in range(chromo_length)])
        self.chromosomes = [Chromosome(bits, mutation_rate) for _ in range(pop_size)]

    def calc_fitness(self, chromosome):
        """
        test how close this chromosome comes to solving the problem
        """
        if chromosome.valid():
            val = chromosome.value()
            if self.value == val:
                return WINNER
            else:
                return math.fabs( 1.0 / ( self.value - val ) )
        else:
            return 0

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
            # no babies
            return papa, mama

        x = random.randint(0, self.chromo_length - 1)

        baby1 = Chromosome(papa.bits[0:x] + mama.bits[x:], self.mutation_rate)
        baby2 = Chromosome(mama.bits[0:x] + papa.bits[x:], self.mutation_rate)

        return baby1, baby2

    def epoch(self):
        """
        run a single generation and return a winner
        """
        self.generation += 1

        winner = None
        # calculate fitness
        for chromosome in self.chromosomes:
            chromosome.fitness = self.calc_fitness(chromosome)
            if chromosome.fitness == WINNER:
                winner = chromosome
                break

        chromosomes = sorted(self.chromosomes, key = lambda c: c.fitness, reverse = True)
        print self.generation, chromosomes[0]

        if winner:
            return winner

        # breed
        new_chromosomes = []
        while len(new_chromosomes) < self.pop_size:
            papa = self.roulette()
            mama = self.roulette()
            if papa and mama:
                baby1, baby2 = self.crossover(papa, mama)
                baby1.mutate()
                baby2.mutate()
                new_chromosomes.append(baby1)
                new_chromosomes.append(baby2)
            else:
                raise RuntimeError('Failed to locate two parents')

        self.chromosomes = new_chromosomes

def main():
    """
    run the program
    """

    from optparse import OptionParser

    parser = OptionParser('main.py <value> [options]')

    parser.add_option("--chromo-length", type='int',
                      dest="chromo_length", default=CHROMO_LEN,
                      help="chromosome length")

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

    if not args:
        parser.error('value is required')

    # begin the program
    value = float(args[0])
    alg = Algorithm(value, options.chromo_length,
                    options.pop_size, options.crossover_rate,
                    options.mutation_rate)

    winner = None
    while not winner and alg.generation < options.max_generations:

        winner = alg.epoch()

if __name__ == '__main__':
    main()

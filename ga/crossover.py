"""
	optimize.ga.crossover
	~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	Implements class for crossover operation between two chromosome.
	:copyright: Hwang.S.J.
	:license: MIT LICENSE 1.0 .
"""

from random import random, randrange
from copy import deepcopy

from .chromosome import Chromosome


class Crossover(object):
    def __init__(self):
        self.parameter = None
        self.methods = {'one_point': self.one_point, 'multi_point': self.multi_point, 'uniform': self.uniform}

    def one_point(self, chromosomes):
        position = randrange(0, len(chromosomes[0].chromosome))

        tmp_chromosome = Chromosome()
        for i in range(len(chromosomes[0].chromosome)):
            if i < position:
                tmp_chromosome.chromosome.append(deepcopy(chromosomes[0].chromosome[i]))
            else:
                tmp_chromosome.chromosome.append(deepcopy(chromosomes[1].chromosome[i]))

        return tmp_chromosome

    def multi_point(self, chromosomes):
        positions = set([])
        while len(positions) < 2:
            positions.add(randrange(0, len(chromosomes[0].chromosome)))
        positions = list(positions)

        positions.sort()
        tmp_chromosome = Chromosome()
        for i in range(len(chromosomes[0].chromosome)):
            if positions[0] <= i < positions[1]:
                tmp_chromosome.chromosome.append(deepcopy(chromosomes[1].chromosome[i]))
            else:
                tmp_chromosome.chromosome.append(deepcopy(chromosomes[0].chromosome[i]))

        return tmp_chromosome

    def uniform(self, chromosomes):
        threshold = self.parameter['threshold'] if 'threshold' in self.parameter else 0.5

        random_values = [random() for _ in range(chromosomes[0].chromosome)]
        tmp_chromosome = Chromosome()

        for i in range(len(random_values)):
            if random_values[i] > threshold:
                tmp_chromosome.chromosome.append(deepcopy(chromosomes[1].chromosome[i]))
            else:
                tmp_chromosome.chromosome.append(deepcopy(chromosomes[0].chromosome[i]))

        return tmp_chromosome

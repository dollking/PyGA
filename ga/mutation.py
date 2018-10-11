"""
	optimize.ga.mutation
	~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	Implements class for mutation operation within chromosome.
	:copyright: Hwang.S.J.
	:license: MIT LICENSE 1.0 .
"""

from copy import deepcopy
from random import random, randrange


class Mutation(object):
    def __init__(self):
        self.parameter = None
        self.methods = {'random_setting': self.random_setting, 'elitist': self.elitist}

    def random_setting(self, chromosome, _):
        mutation_count = self.parameter['mutation_count'] if 'mutation_count' in self.parameter else 1
        mutation_probability = self.parameter['mutation_probability'] if 'mutation_probability' in self.parameter else 0.3

        for _ in range(mutation_count):
            if random() <= mutation_probability:
                pos = randrange(0, len(chromosome.chromosome))
                chromosome.mutate(pos)

        return chromosome

    def elitist(self, chromosome, population):
        mutation_count = self.parameter['mutation_count'] if 'mutation_count' in self.parameter else 1
        mutation_probability = self.parameter['mutation_probability'] if 'mutation_probability' in self.parameter else 0.3
        elite_rate = self.parameter['elite_rate'] if 'elite_rate' in self.parameter else 0.6

        for _ in range(mutation_count):
            if random() <= mutation_probability:
                pos = randrange(0, len(chromosome.chromosome))
                mother_chromosome_gene = population[randrange(0, int(len(population) * elite_rate))].chromosome[pos]
                chromosome.mutate(pos, deepcopy(mother_chromosome_gene))

        return chromosome

    @property
    def help(self):
        return '''
        MUTATION - Mutation is that select gene randomly and change. It do not always operate.
        random_setting: The mutations randomly within a range set earlier.
                    (parameter: {'mutation_count': integer_data(1-chromosome length), 'mutation_probability': float_data(0.0-1.0)})
        elitist: Mutation value is selected in elite chromosome.
                    (parameter: {'mutation_count': int_data(1-chromosome length), 'mutation_probability': float_data(0.0-1.0), 'elite_rate': float_data(0.0-1.0)})
        '''

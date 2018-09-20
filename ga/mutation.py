"""
	optimize.ga.mutation
	~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	Implements class for mutation operation within chromosome.
	:copyright: Hwang.S.J.
	:license: MIT LICENSE 1.0 .
"""

from random import random, randrange


class Mutation(object):
    def __init__(self):
        self.parameter = None
        self.mutation_rate = None #mutation_rate
        self.methods = {'random_setting': self.random_setting}

    def random_setting(self, chromosome):
        mutation_probability = self.parameter['mutation_probability'] if 'mutation_probability' in self.parameter else 0.3
        if random() <= mutation_probability:
            pos = randrange(0, len(chromosome.chromosome))
            chromosome.mutate(pos)

        return chromosome
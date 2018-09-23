"""
	optimize.ga.chromosome
	~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	Implements class for manage chromosome.
	:copyright: Hwang.S.J.
	:license: MIT LICENSE 1.0 .
"""

from .gene import Gene


class Chromosome(object):
    def __init__(self):
        self.chromosome = []

    def add_gene(self, dtype, value_range, isNormal=False):
        self.chromosome.append(Gene(dtype, value_range, isNormal))

    def mutate(self, index, gene_data=None):
        if gene_data:
            self.chromosome[index] = gene_data
        else:
            self.chromosome[index].mutation()

    @property
    def get_values(self):
        return [i.value for i in self.chromosome]

    def __str__(self):
        return str(self.get_values)

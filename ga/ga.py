"""
	optimize.ga.ga
	~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	Implements class for setting and running to use genetic algorithm.
	:copyright: Hwang.S.J.
	:license: MIT LICENSE 1.0 .
"""

from copy import deepcopy

from .mutation import Mutation
from .crossover import Crossover
from .selection import ChromosomeSelection, SurvivorSelection


class GeneticAlgorithm(object):
    def __init__(self, fitness_func, terminate_threshold, chromosome, population_size, condition='max', epoch=1000):
        self.epoch = epoch
        self.fitness_function = fitness_func
        self.terminate_threshold = terminate_threshold
        self.condition = condition

        self.sample_chromosome = chromosome
        self.population_size = population_size

        self.selection = ChromosomeSelection(self.population_size)
        self.crossover = Crossover()
        self.mutation = Mutation()
        self.survivor = SurvivorSelection(self.population_size)

        self.select_method = None
        self.crossover_method = None
        self.mutation_method = None
        self.survivor_method = None

        self.population = []
        self.make_chromosome()

    def add_method(self, step, method_name, **kwargs):
        if step == 'selection':
            self.select_method = self.selection.methods[method_name]
            self.selection.parameter = kwargs

        elif step == 'crossover':
            self.crossover_method = self.crossover.methods[method_name]
            self.crossover.parameter = kwargs

        elif step == 'mutation':
            self.mutation_method = self.mutation.methods[method_name]
            self.mutation.parameter = kwargs

        elif step == 'survivor':
            self.survivor_method = self.survivor.methods[method_name]
            self.survivor.parameter = kwargs

        else:
            raise ValueError

    def make_chromosome(self):
        for _ in range(self.population_size):
            self.population.append(deepcopy(self.sample_chromosome))

            for gene in self.population[-1].chromosome:
                gene.get_value()

    def run(self):
        cnt = 0

        isReverse = True if self.condition == 'max' else False
        while cnt < self.epoch:
            self.population.sort(key=lambda x: self.fitness_function(x.get_value_list()), reverse=isReverse)
            self.selection.set_current_fitness(self.population, self.fitness_function)

            if (self.condition == 'max' and self.selection.current_fitness[0] > self.terminate_threshold) or \
                    (self.condition == 'min' and self.selection.current_fitness[0] < self.terminate_threshold):
                break

            next_population = self.survivor_method()
            while len(next_population) < self.population_size:
                next_population.append(self.mutation_method(self.crossover_method(self.select_method())))

            self.selection.init_current_fitness()
            self.population = next_population

            cnt += 1

        print(self.population[0].get_value_list())
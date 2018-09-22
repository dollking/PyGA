"""
	optimize.ga.ga
	~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	Implements class for setting and running to use genetic algorithm.
	:copyright: Hwang.S.J.
	:license: MIT LICENSE 1.0 .
"""

from copy import deepcopy
from multiprocessing import cpu_count, Pool

from .mutation import Mutation
from .crossover import Crossover
from .selection import ChromosomeSelection, SurvivorSelection


class GeneticAlgorithm(object):
    def __init__(self, fitness_func, terminate_threshold, chromosome, population_size,
                 condition='max', thread_count=1, epoch=1000):
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
        self.current_fitness = []
        self.make_chromosome()
        self.core_count = thread_count if thread_count <= (cpu_count() - 1) else (cpu_count() - 1)

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

    def operation_set(self, _):
        return self.mutation_method(self.crossover_method(self.select_method(self.current_fitness, self.population)))

    def run(self):
        cnt = 0
        pool = Pool(self.core_count)
        isReverse = True if self.condition == 'max' else False

        while cnt < self.epoch:
            self.population.sort(key=lambda x: self.fitness_function(x.get_value_list()), reverse=isReverse)
            self.current_fitness = [self.fitness_function(i.get_value_list()) for i in self.population]

            if (self.condition == 'max' and self.current_fitness[0] > self.terminate_threshold) or \
                    (self.condition == 'min' and self.current_fitness[0] < self.terminate_threshold):
                break

            next_population = self.survivor_method(self.current_fitness, self.population)
            next_population.extend(pool.map(self.operation_set, range(self.population_size - len(next_population))))

            self.population = next_population

            cnt += 1

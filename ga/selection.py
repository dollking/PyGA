"""
	optimize.ga.mutation
	~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	Implements class for all selection operation to select chromosome for crossover operation and using next generation.
	:copyright: Hwang.S.J.
	:license: MIT LICENSE 1.0 .
"""

from random import randrange, uniform, random


class Selection(object):
    population = []
    current_fitness = []
    def __init__(self, population_size):
        self.parameter = None
        self.population_size = population_size


    def set_current_fitness(self, population, fitness_func):
        if not len(self.current_fitness):
            for i in range(self.population_size):
                self.population.append(population[i])
                self.current_fitness.append(fitness_func(population[i].get_value_list()))

    def init_current_fitness(self):
        self.population = []
        self.current_fitness = []


class ChromosomeSelection(Selection):
    def __init__(self, population_size):
        super(ChromosomeSelection, self).__init__(population_size)
        self.methods = {'roulette': self.roulette, 'tournament': self.tournament,
                        'ranking': self.ranking, 'elitist': self.elitist}

    def roulette(self):
        isUniform = self.parameter['isUniform'] if 'isUniform' in self.parameter else True

        tmp_set = set([])
        if isUniform:
            while len(tmp_set) < 2:
                tmp_index = randrange(0, self.population_size)
                tmp_set.add(tmp_index)

        else:
            probability_list = []
            worst = Selection.current_fitness[-1]
            best = Selection.current_fitness[0]

            for i in Selection.current_fitness:
                probability_list.append(abs(2 * worst - i - best) / 3.)

            while len(tmp_set) < 2:
                _sum = 0.
                select_point = uniform(0, sum(probability_list))
                for i in range(len(probability_list)):
                    _sum += probability_list[i]
                    if select_point < _sum:
                        tmp_set.add(i)

        return [Selection.population[i] for i in tmp_set]

    def tournament(self):
        threshold = self.parameter['threshold'] if 'threshold' in self.parameter else 0.5

        tmp_set = set([])
        while len(tmp_set) < 2:
            if random() < threshold:
                tmp_set.add(self.roulette()[0])
            else:
                tmp_set.add(self.roulette()[1])

        return [Selection.population[i] for i in tmp_set]

    def ranking(self):
        tmp_set = set([])

        probability_list = []
        _max = max(Selection.current_fitness)
        _min = min(Selection.current_fitness)

        for i in Selection.current_fitness:
            probability_list.append(_max + (_min - _max) * i / (self.population_size - 1))

        while len(tmp_set) < 2:
            _sum = 0.
            select_point = uniform(0, sum(probability_list))
            for i in range(len(probability_list)):
                _sum += probability_list[i]
                if select_point < _sum:
                    tmp_set.add(i)

        return [Selection.population[i] for i in tmp_set]

    def elitist(self):
        elite_rate = self.parameter['elite_rate'] if 'elite_rate' in self.parameter else 0.3
        exception_rate = self.parameter['exception_rate'] if 'exception_rate' in self.parameter else 0.0
        tmp_set = set([])

        while len(tmp_set) < 2:
            if random() < exception_rate:
                tmp_set.add(randrange(int(self.population_size * elite_rate), self.population_size))

            else:
                tmp_set.add(randrange(0, int(self.population_size * elite_rate)))

        return [Selection.population[i] for i in tmp_set]


class SurvivorSelection(Selection):
    def __init__(self, population_size):
        super(SurvivorSelection, self).__init__(population_size)
        self.methods = {'roulette': self.roulette, 'elitist': self.elitist}

    def roulette(self):
        isUniform = self.parameter['isUniform'] if 'isUniform' in self.parameter else True
        selection_rate = self.parameter['selection_rate'] if 'selection_rate' in self.parameter else 0.6

        selection_size = int(self.population_size * selection_rate)

        tmp_set = set([])
        if isUniform:
            while len(tmp_set) < selection_size:
                tmp_index = randrange(0, self.population_size)
                tmp_set.add(tmp_index)

        else:
            probability_list = []
            worst = Selection.current_fitness[-1]
            best = Selection.current_fitness[0]

            for i in Selection.current_fitness:
                probability_list.append(abs(2 * worst - i - best) / 3.)

            while len(tmp_set) < selection_size:
                _sum = 0.
                select_point = uniform(0, sum(probability_list))
                for i in range(len(probability_list)):
                    _sum += probability_list[i]
                    if select_point < _sum:
                        tmp_set.add(i)

        return [Selection.population[i] for i in tmp_set]

    def elitist(self):
        elite_rate = self.parameter['elite_rate'] if 'elite_rate' in self.parameter else 0.3
        exception_rate = self.parameter['exception_rate'] if 'exception_rate' in self.parameter else 0.0
        selection_rate = self.parameter['selection_rate'] if 'selection_rate' in self.parameter else 0.6
        selection_size = int(self.population_size * selection_rate)

        tmp_set = set([])
        piv = max(selection_size, int(self.population_size * elite_rate))
        while len(tmp_set) < selection_size:
            if random() < exception_rate:
                tmp_set.add(randrange(piv, self.population_size))

            else:
                tmp_set.add(randrange(0, piv))

        return [Selection.population[i] for i in tmp_set]

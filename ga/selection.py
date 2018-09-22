"""
	optimize.ga.mutation
	~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	Implements class for all selection operation to select chromosome for crossover operation and using next generation.
	:copyright: Hwang.S.J.
	:license: MIT LICENSE 1.0 .
"""

from random import randrange, uniform, random


class ChromosomeSelection(object):
    def __init__(self, population_size):
        self.parameter = None
        self.population_size = population_size
        self.methods = {'roulette': self.roulette, 'tournament': self.tournament,
                        'ranking': self.ranking, 'elitist': self.elitist}

    def roulette(self, current_fitness, population):
        isUniform = self.parameter['isUniform'] if 'isUniform' in self.parameter else True

        tmp_set = set([])
        if isUniform:
            while len(tmp_set) < 2:
                tmp_index = randrange(0, self.population_size)
                tmp_set.add(tmp_index)

        else:
            probability_list = []
            worst = current_fitness[-1]
            best = current_fitness[0]

            for i in current_fitness:
                probability_list.append(abs(2 * worst - i - best) / 3.)

            while len(tmp_set) < 2:
                _sum = 0.
                select_point = uniform(0, sum(probability_list))
                for i in range(len(probability_list)):
                    _sum += probability_list[i]
                    if select_point < _sum:
                        tmp_set.add(i)

        return [population[i] for i in tmp_set]

    def tournament(self, current_fitness, population):
        threshold = self.parameter['threshold'] if 'threshold' in self.parameter else 0.5

        tmp_set = set([])
        while len(tmp_set) < 2:
            if random() < threshold:
                tmp_set.add(self.roulette()[0])
            else:
                tmp_set.add(self.roulette()[1])

        return [population[i] for i in tmp_set]

    def ranking(self, current_fitness, population):
        tmp_set = set([])

        probability_list = []
        _max = max(current_fitness)
        _min = min(current_fitness)

        for i in current_fitness:
            probability_list.append(_max + (_min - _max) * i / (self.population_size - 1))

        while len(tmp_set) < 2:
            _sum = 0.
            select_point = uniform(0, sum(probability_list))
            for i in range(len(probability_list)):
                _sum += probability_list[i]
                if select_point < _sum:
                    tmp_set.add(i)

        return [population[i] for i in tmp_set]

    def elitist(self, current_fitness, population):
        elite_rate = self.parameter['elite_rate'] if 'elite_rate' in self.parameter else 0.3
        exception_rate = self.parameter['exception_rate'] if 'exception_rate' in self.parameter else 0.0
        tmp_set = set([])

        while len(tmp_set) < 2:
            if random() < exception_rate:
                tmp_set.add(randrange(int(self.population_size * elite_rate), self.population_size))

            else:
                tmp_set.add(randrange(0, int(self.population_size * elite_rate)))

        return [population[i] for i in tmp_set]


class SurvivorSelection(object):
    def __init__(self, population_size):
        self.parameter = None
        self.population_size = population_size
        self.methods = {'roulette': self.roulette, 'elitist': self.elitist}

    def roulette(self, current_fitness, population):
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
            worst = current_fitness[-1]
            best = current_fitness[0]

            for i in current_fitness:
                probability_list.append(abs(2 * worst - i - best) / 3.)

            while len(tmp_set) < selection_size:
                _sum = 0.
                select_point = uniform(0, sum(probability_list))
                for i in range(len(probability_list)):
                    _sum += probability_list[i]
                    if select_point < _sum:
                        tmp_set.add(i)

        return [population[i] for i in tmp_set]

    def elitist(self, current_fitness, population):
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

        return [population[i] for i in tmp_set]

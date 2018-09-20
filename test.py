from ga.ga import GeneticAlgorithm
from ga.chromosome import Chromosome

def fitness(data):
    limit = 15
    items = {0: [10, 2], 1: [5, 5], 2: [1, 1], 3: [3, 2], 4: [4, 5], 5: [3, 3]}

    val = 0.0
    vol = 0.0
    for i in range(len(data)):
        if data[i]:
            val += items[i][1]
            vol += items[i][0]

    if vol > limit:
        return 0

    return val

if __name__ == '__main__':
    # set chromosome shape
    chromosome = Chromosome()
    chromosome.add_gene('choice', [0, 1])
    chromosome.add_gene('choice', [0, 1])
    chromosome.add_gene('choice', [0, 1])
    chromosome.add_gene('choice', [0, 1])
    chromosome.add_gene('choice', [0, 1])
    chromosome.add_gene('choice', [0, 1])

    # make object for genetic algorithm
    genetic = GeneticAlgorithm(fitness, 50, chromosome, 100)

    # set operation using genetic algorithm
    genetic.add_method('selection', 'roulette')
    genetic.add_method('crossover', 'one_point')
    genetic.add_method('mutation', 'random_setting')
    genetic.add_method('survivor', 'elitist')

    # learning
    genetic.run()

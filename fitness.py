import math
import collections

__author__ = 'gorigan'


class Fitness(object):
    def fitness_function(self):
        raise NotImplementedError('subclasses must override fitness_function()!')

    def eval(self, population, data, pop_size):
        for individual in population:
            if individual.get_fitness() == 0.0:
                individual_fitness = 0.0
                for data_row in data:
                        if len(data_row) > 0:
                            generated_value = individual.eval(data_row)
                            individual_fitness += self.fitness_function(generated_value, 0)

                individual.set_fitness(individual_fitness)

        population.sort(key=lambda x: x.get_fitness())
        population = population[0:pop_size]
        avg_fitness = 0

        duplicated = 0
        representations = []
        for idx, individual in enumerate(population):
            representations.append(str(individual))
            avg_fitness += individual.get_fitness()
        avg_fitness /= pop_size

        counter = collections.Counter(representations)
        for val in counter.values():
            val -= 1
            duplicated += val
        return population, avg_fitness, duplicated


class ErrorAbs(Fitness):
    def fitness_function(self, generated_value, target_value):
        fitness = math.fabs(generated_value - target_value)
        return fitness

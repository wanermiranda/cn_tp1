import math

__author__ = 'gorigan'


class Fitness(object):
    def fitness_function(self):
        raise NotImplementedError('subclasses must override fitness_function()!')

    def eval(self, population, data):
        for individual in population:
            if individual.get_fitness() == 0.0:
                individual_fitness = 0.0
                for data_row in data:
                        if len(data_row) > 0:
                            # print 'data_row', data_row
                            # target_value = data_row[len(data_row) - 1]
                            # print 'target', target_value
                            generated_value = individual.eval(data_row)
                            individual_fitness += self.fitness_function(generated_value, 0)

                individual.set_fitness(individual_fitness)

        population.sort(key=lambda x: x.get_fitness())
        for individual in population[:1]:
            print 'Best ind:', individual
            print 'Fitness =', individual.get_fitness()

        return population


class ErrorAbs(Fitness):
    def fitness_function(self, generated_value, target_value):
        fitness = math.fabs(generated_value - target_value)
        return fitness

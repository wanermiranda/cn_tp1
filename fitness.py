import math

__author__ = 'gorigan'


class Fitness(object):
    def function(self):
        raise NotImplementedError('subclasses must override foo()!')

    def eval(self, population, data):
        for individual in population:
            individual_fitness = 0.0
            for data_row in data:
                    if len(data_row) > 0:
                        # print 'data_row', data_row
                        target_value = data_row[len(data_row) - 1]
                        # print 'target', target_value
                        generated_value = individual.eval(data_row)
                        individual_fitness += self.function(generated_value, target_value)

            individual.set_fitness(individual_fitness)

        population.sort(key=lambda x: x.get_fitness())
        for individual in population[:1]:
            print individual, ' = ', individual.get_fitness()

        return population


class QuadError(Fitness):
    def function(self, generated_value, target_value):
        return math.fabs(generated_value - target_value)

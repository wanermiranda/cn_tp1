import math
import collections

DECIMALS = (10 * 16)

__author__ = 'gorigan'


class Fitness(object):

    def eval(self, population, data, pop_size, target_fitness):
        for individual in population:
            self.eval_individual(data, individual, target_fitness)
            # print individual, 'Fitness:\n', individual.get_fitness()

        population.sort(key=lambda x: x.get_fitness())
        population = population[0:pop_size]

        avg_fitness, duplicated = self.get_stats(pop_size, population)
        return population, avg_fitness, duplicated

    @staticmethod
    def get_stats(pop_size, population):
        duplicated = 0
        representations = []
        avg_fitness = 0
        for idx, individual in enumerate(population):
            representations.append(str(individual))
            avg_fitness += individual.get_fitness()
        avg_fitness /= pop_size
        counter = collections.Counter(representations)
        for val in counter.values():
            val -= 1
            duplicated += val
        return avg_fitness, duplicated

    def eval_individual(self, data, individual, target_fitness):
        raise NotImplemented


class MSEFitness(Fitness):

    def eval_individual(self, data, individual, target_fitness):
        if individual.get_fitness() == 0.0:
            individual_fitness = 0.0
            # avg = 0
            # values = []
            for data_row in data:
                if len(data_row) > 0:
                    generated_value = individual.eval(data_row)
                    # target_fitness = - math.pow(data_row[len(data_row)-1], 2)
                    diff = (generated_value - target_fitness)
                    # values.append(diff)
                    # avg += abs(diff)
                    individual_fitness += math.fabs(diff)

            # avg /= len(data)
            # variance = 0
            # for value in values:
            #     variance += math.pow(value - avg, 2)
            #+ math.sqrt(variance / len(data)
            koza = math.pow(individual_fitness, 2) / len(data)

            individual.set_fitness(koza)



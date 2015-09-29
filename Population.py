import random
import Individual as ind
import copy
__author__ = 'Waner Miranda'


def sample_k_values(seq, k):
    if not 0 <= k <= len(seq):
        raise ValueError('Required that 0 <= sample_size <= population_size')
    internal_list = []
    values_picked = 0
    for i, value in enumerate(seq):
        prob = (k-values_picked)/(len(seq)-i)
        if random.random() < prob:
            internal_list.append(value)
            values_picked += 1

    return internal_list


class PopulationHandler:

    def __init__(self, min_depth=2, max_depth=3, pop_size=500, terminals_chance=0.5, non_terminals_chance=0.5,
                 non_terminals=['Add', 'Subtract', 'ProtectedDiv', 'Multiply'],
                 terminals=['FloatTerminal', 'ArrayVariableTerminal'], variables=['x']):
        self._min_depth = min_depth
        self._max_depth = max_depth
        self._pop_size = pop_size
        self._terminals_chance = terminals_chance
        self._non_terminals_chance = non_terminals_chance
        self._non_terminals = non_terminals
        self._terminals = terminals
        self._variables = variables
        self._population = []

    def build_population(self):
        for pop in range(self._pop_size):
            individual = ind.Individual(self._non_terminals, self._terminals, self._min_depth, self._max_depth,
                                        self._terminals_chance, self._non_terminals_chance, self._variables)
            print 'ind:', self._population.__len__()+1
            print individual
            # individual1 = copy.deepcopy(individual)
            # individual1.mutate()
            # print 'source', individual
            # print 'clone ', individual1
            self._population.append(individual)

    def eval(self, fitness, data):
        self._population = fitness.eval(self._population, data)

    def produce_new_population(self, cross_over_chance, mutation_chance):
        if (cross_over_chance + mutation_chance) > 1:
            raise ValueError('The sum of the chances must be equals to 1 or less.')
        selected_individuals = self._population[:self._pop_size]
        cross_overs = int(self._pop_size * cross_over_chance)
        mutations = int(self._pop_size * mutation_chance)
        reproductions = int(self._pop_size - (cross_overs + mutations))
        selected_cross_overs = sample_k_values(selected_individuals, cross_overs)
        selected_mutations = sample_k_values(selected_individuals, mutations)

        print 'Starting mutation pipeline. '
        for individual in selected_mutations:
            individual.mutate()

        print 'Starting cross over pipeline. '
        group_1 = selected_cross_overs[:len(selected_cross_overs)/2]
        group_2 = selected_cross_overs[len(selected_cross_overs)/2:]
        how_much = len(group_1) if len(group_1) < len(group_2) else len(group_2)
        for position in range(how_much):
            individual_1 = group_1[position]
            individual_2 = group_2[position]
            if not individual_1.equals(individual_2):
                son_1 = copy.deepcopy(individual_1)
                son_2 = copy.deepcopy(individual_2)
                selected_node1 = copy.deepcopy(son_1.select_node())
                selected_node2 = copy.deepcopy(son_2.select_node())
                son_1.cross_over(selected_node1, selected_node2)
                son_2.cross_over(selected_node2, selected_node1)
                print 'Crossing '
                print individual_1
                print individual_2
                print son_1
                print son_2

        selected_reproductions = sample_k_values(selected_individuals, reproductions)
        self._population = selected_reproductions + selected_mutations + group_1 + group_2
        print "Population size: ", len(self._population)




import random
import Individual as ind
import copy
__author__ = 'Waner Miranda'


class PopulationHandler:

    def tournament(self, target_list):
        best_ind = None
        for i in range(self._tournament_size):
            index = random.choice(range(len(target_list)))
            if (best_ind is None) or (best_ind.get_fitness() < target_list[index].get_fitness()):
                best_ind = target_list[index]
        target_list.remove(best_ind)
        return best_ind

    def tournament_selection(self, target_list, n_individuals):
        if not 0 <= n_individuals <= len(target_list):
            raise ValueError('Required that 0 <= sample_size <= population_size')
        internal_list = []
        for i in range(n_individuals):
            internal_list.append(self.tournament(target_list))

        return internal_list

    def __init__(self, min_depth=2, max_depth=7, pop_size=500, terminals_chance=0.5, non_terminals_chance=0.5,
                 tournament_size=5, elitism=False,
                 non_terminals=['Add', 'Subtract', 'ProtectedDiv', 'Multiply'],
                 terminals=['ArrayVariableTerminal'], variables=['x']):
        self._min_depth = min_depth
        self._max_depth = max_depth
        self._pop_size = pop_size
        self._terminals_chance = terminals_chance
        self._non_terminals_chance = non_terminals_chance
        self._non_terminals = non_terminals
        self._terminals = terminals
        self._variables = variables
        self._population = []
        self._tournament_size = tournament_size
        self._elitism = elitism

    def build_population(self):
        for pop in range(self._pop_size):
            individual = ind.Individual(self._non_terminals, self._terminals, self._min_depth, self._max_depth,
                                        self._terminals_chance, self._non_terminals_chance, self._variables)
            print 'ind:', self._population.__len__()+1
            print individual
            # print 'Depth', individual.get_tree().get_tree_depth(), individual._max_depth
            self._population.append(individual)

    def eval(self, fitness, data):
        self._population, avg_fitness, duplicated = fitness.eval(self._population, data, self._pop_size)
        print 'Best',
        self._population[0].print_stats()
        print 'Worst',
        self._population[self._pop_size-1].print_stats()
        print 'Avg Fitness =', avg_fitness
        print 'Duplicated =', duplicated

    def do_evolution(self, cross_over_chance, mutation_chance):
        if (cross_over_chance + mutation_chance) > 1:
            raise ValueError('The sum of the chances must be equals to 1 or less.')
        selected_individuals = self._population
        if self._elitism:
            elite_individual = self._population[0]
            self._population.remove(elite_individual)
            pop_size = self._pop_size - 1
        else:
            pop_size = self._pop_size

        cross_overs = int(pop_size * cross_over_chance)
        mutations = int(pop_size * mutation_chance)
        reproductions = int(pop_size - (cross_overs + mutations))

        selected_reproductions = self.tournament_selection(selected_individuals, reproductions)
        selected_cross_overs = self.tournament_selection(selected_individuals, cross_overs)
        selected_mutations = self.tournament_selection(selected_individuals, mutations)

        # print 'Starting mutation pipeline. '
        for individual in selected_mutations:
            individual.mutate()

        # print 'Starting cross over pipeline. '
        group_1 = selected_cross_overs[:len(selected_cross_overs)/2]
        group_2 = selected_cross_overs[len(selected_cross_overs)/2:]
        how_much = len(group_1) if len(group_1) < len(group_2) else len(group_2)
        crossed_overs = []
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
                if son_1.get_tree_depth() > self._max_depth:
                    crossed_overs.append(individual_1)
                else:
                    crossed_overs.append(son_1)

                if son_2.get_tree_depth() > self._max_depth:
                    crossed_overs.append(individual_2)
                else:
                    crossed_overs.append(son_2)

            else:
                crossed_overs.append(individual_1)

        self._population = selected_reproductions + selected_mutations + selected_cross_overs + crossed_overs
        if self._elitism:
            self._population = [elite_individual] + self._population
        print "Population size: ", len(self._population)




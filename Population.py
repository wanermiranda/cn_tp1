import random
import Individual as ind

__author__ = 'Waner Miranda'


class GrowthPopulationBuilder:
    def __init__(self, min_depth=2, max_depth=6, pop_size=500, terminals_chance=0.7, non_terminals_chance=0.3,
                 non_terminals=['Add', 'Subtract', 'ProtectedDiv', 'Multiply'], terminals=['FloatTerminal']):
        self._min_depth = min_depth
        self._max_depth = max_depth
        self._pop_size = pop_size
        self._terminals_chance = terminals_chance
        self._non_terminals_chance = non_terminals_chance
        self._non_terminals = non_terminals
        self._terminals = terminals
        self._population = []

    def build_population(self):
        for pop in range(self._pop_size):
            individual = ind.Individual(self._non_terminals, self._terminals, self._min_depth, self._max_depth,
                                        self._terminals_chance, self._non_terminals_chance)
            self._population.append(individual)
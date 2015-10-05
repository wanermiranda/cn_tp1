#!/bin/python
from Population import PopulationHandler
import numpy as np
import sys
import getopt
import fitness as ft

__author__ = 'Waner Miranda'


class MultiVariableRegression:
    """
        Class designed to contain the main definition of the problem to be solved by the GP
    """
    def __init__(self, dataset, population, generations, tournament_size, elitism,
                 mutation_chance, cross_over_chance, vars, yacht, skewed):

        """
        @param dataset: list
        @param population: int
        @param generations: int
        @param tournament_size: int
        @param elitism: Boolean
        @param mutation_chance: float
        @param cross_over_chance: float
        @param vars: list
        """
        self._dataset = []
        # Convert the dataset form the text file into a list of floats
        for line in open(dataset):
            value_line = []
            for value in line.rstrip('\n\r').split():
                if value.strip(' ').__len__() != 0:
                    value_line.append(float(value))
            if value_line:
                self._dataset.append(value_line)
        self._dataset = np.array(self._dataset)
        print self._dataset.shape

        print '============================================================================'
        print 'Build initial population'
        # Circles and Ellipses can be expressed in forms like (x/a)^2 + (y/b)^2 = 1
        # The target fitness was set to 1
        target_fitness = 1.0 
        terminals = ['ArrayVariableFloat']
        if yacht:
            target_fitness = None
            non_terminals = ['Add', 'Multiply', 'Pow2', 'Subtract', 'ProtectedDiv']            
        else:
            non_terminals = ['Add', 'Multiply', 'Pow2']

        if skewed:
            terminals += ['ArrayVariableSkewed']
        
            
        
        pop_builder = PopulationHandler(pop_size=population, tournament_size=tournament_size, elitism=elitism,
                                        dataset=self._dataset, variables=vars, fitness=ft.MSEFitness(),
                                        target_fitness=target_fitness, non_terminals=non_terminals, terminals=terminals)
        best = 1
        tries = 0
        # while best >= 1:
        pop_builder.build_population()
        best = pop_builder.eval()
        # tries += 1
        # print 'Try ', tries, ' Best ', best

        for generation in range(generations):
            print '============================================================================'
            print 'Evaluate Gen ', generation + 1
            new_pop, better_than_dads = pop_builder.do_evolution(cross_over_chance, mutation_chance)

            print 'New Population', new_pop
            print 'Better than Dads', better_than_dads

            pop_builder.eval()
        exit(0)


def usage():
    print 'example: main.py -f dataset.txt -p 500 -g 500 -t 7 -m 0.39 -x 0.6 | -e | [-y|-s]' \
          '\n --dataset_file=dataset.txt --population=500 --generations=500  --tournament_size=7 ' \
          ' --mutation=0.39 --cross_over=0.6 --elitism | [--yacht|--skewed]'

def main():
    dataset_file = ""

    try:
        arg_list = sys.argv[1:]
        opts, args = getopt.getopt(arg_list, 'f:p:g:t:m:x:v:eysh', ['dataset_file=', 'population=', 'mutation=',
                                                                'cross_over=', 'generations=', 'tournament_size=',
                                                                'vars=','elitism', 'yacht','skewed','help'])
    except getopt.GetoptError:
        print 'okey'
        raise
    population = 500
    generations = 500
    mutation = 0.35
    cross_over = 0.60
    tournament_size = 7
    vars = ['x', 'y']
    elitism = False
    yacht=False
    skewed = False
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            exit(0)
        elif opt in ("-f", "--dataset_file"):
            dataset_file = arg
            print 'dataset_file=', arg
        elif opt in ("-p", "--population"):
            population = int(arg)
            print 'population=', arg
        elif opt in ("-g", "--generations"):
            generations = int(arg)
            print 'generations=', arg
        elif opt in ("-t", "--tournament_size"):
            tournament_size = int(arg)
            print 'tournament_size=', arg
        elif opt in ("-m", "--mutation"):
            mutation = float(arg)
            print 'mutation=', arg
        elif opt in ("-x", "--cross_over"):
            cross_over = float(arg)
            print 'cross_over=', arg
        elif opt in ("-v", "--vars"):
            vars = arg.split()
            print 'cross_over=', arg
        elif opt in ("-e", "--elitism"):
            elitism = True
            print 'elitism=', elitism
        elif opt in ("-y", "--yacht"):
            yacht=True
            vars = ['a', 'b', 'c', 'd', 'e', 'f']
            print 'yacht=', yacht            
            print 'vars=', vars      
        elif opt in ("-s", "--skewed"):
            skewed = True
            print 'skewed=', skewed

    MultiVariableRegression(dataset_file, population, generations, tournament_size, elitism, mutation, cross_over, vars, yacht, skewed)


if __name__ == "__main__":
    main()

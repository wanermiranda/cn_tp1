#!/bin/python
from Population import PopulationHandler

__author__ = 'Waner Miranda'
import numpy as np
import sys
import getopt
import fitness as ft


class MultiVariableRegression:
    def __init__(self, dataset, population, generations, tournament_size, elitism, mutation_chance, cross_over_chance):
        """

        :type dataset: unicode
        :type config: unicode
        """
        self._dataset = []
        for line in open(dataset):
            value_line = []
            for value in line.rstrip('\n\r').split():
                if value.strip(' ').__len__() != 0:
                    value_line.append(float(value))
            if value_line:
                self._dataset.append(value_line)
        self._dataset = np.array(self._dataset)
        print self._dataset.shape
        r, c = self._dataset.shape[:2]
        if c == 3:
            self._dataset = self._dataset[:, 1:]
        # print self._dataset
        print '============================================================================'
        print 'Build initial population'
        pop_builder = PopulationHandler(pop_size=population, tournament_size=tournament_size, elitism=elitism,
                                        dataset=self._dataset, variables=['x', 'y'], fitness=ft.ErrorAbs())
        pop_builder.build_population()
        pop_builder.eval()
        for generation in range(generations):
            print '============================================================================'
            print 'Evaluate Gen ', generation
            new_pop, better_than_dads = pop_builder.do_evolution(cross_over_chance, mutation_chance)

            print 'New Population', new_pop
            print 'Better than Dads', better_than_dads

            pop_builder.eval()
        exit(0)


def usage():
    print 'example: main.py -f dataset.txt -p 500 -g 500 -t 7 -m 0.39 -x 0.6 -e' \
          '\n --dataset_file=dataset.txt --population=500 --generations=500  --tournament_size=7 ' \
          ' --mutation=0.39 --cross_over=0.6 --elitism'


def main():
    dataset_file = ""

    try:
        arg_list = sys.argv[1:]
        opts, args = getopt.getopt(arg_list, 'f:p:g:t:m:x:eh', ['dataset_file=', 'population=', 'mutation=',
                                                                'cross_over=', 'generations=', 'tournament_size=',
                                                                'elitism', 'help'])
    except getopt.GetoptError:
        usage()
        raise
    population = 500
    generations = 500
    mutation = 0.05
    cross_over = 0.9
    tournament_size = 7
    elitism = False
    for opt, arg in opts:
        if opt == '-h':
            usage()
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
        elif opt in ("-e", "--elitism"):
            elitism = True
            print 'elitism=', elitism

    MultiVariableRegression(dataset_file, population, generations, tournament_size, elitism, mutation, cross_over)


if __name__ == "__main__":
    main()
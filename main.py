#!/bin/python
from Population import PopulationHandler

__author__ = 'Waner Miranda'
import numpy as np
import sys
import getopt
import fitness as ft


class MultiVariableRegression:
    def __init__(self, dataset, population, generations, tournament_size, elitism):
        """

        :type dataset: unicode
        :type config: unicode
        """
        self._dataset = []
        cross_over_chance = 0.60
        mutation_chance = 0.39
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

        print 'Build initial population'
        pop_builder = PopulationHandler(pop_size=population, tournament_size=tournament_size, elitism=elitism,
                                        variables=['x', 'y'])
        pop_builder.build_population()
        pop_builder.eval(ft.ErrorAbs(), self._dataset)
        for generation in range(generations):
            print 'Evaluate Gen ', generation
            pop_builder.do_evolution(cross_over_chance, mutation_chance)
            pop_builder.eval(ft.ErrorAbs(), self._dataset)
            pop_builder.select_fittest()
        exit(0)


def usage():
    print 'example: main.py -f dataset.txt -p 500 -g 500 -t 7 -e' \
          '\n --dataset_file=dataset.txt --population=500 --generations=500  --tournament_size=7 --elitism'


def main():
    dataset_file = ""

    try:
        arg_list = sys.argv[1:]
        opts, args = getopt.getopt(arg_list, 'f:p:g:t:eh', ['dataset_file=', 'population=',
                                                            'generations=', 'tournament_size=', 'elitism', 'help'])
    except getopt.GetoptError:
        usage()
        raise
    population = 500
    generations = 500
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
        elif opt in ("-e", "--elitism"):
            elitism = True
            print 'elitism=', elitism

    MultiVariableRegression(dataset_file, population, generations, tournament_size, elitism)


if __name__ == "__main__":
    main()
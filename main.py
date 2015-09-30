#!/bin/python
from Population import PopulationHandler

__author__ = 'Waner Miranda'
import numpy as np
import sys
import getopt
import fitness as ft


class MultiVariableRegression:
    def __init__(self, dataset, config):
        """

        :type dataset: unicode
        :type config: unicode
        """

        self._config = config
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
        pop_builder = PopulationHandler()
        pop_builder.build_population()
        pop_builder.eval(ft.QuadError(), self._dataset)
        for generation in range(1000):
            print 'Evaluate Gen ', generation
            pop_builder.do_evolution(cross_over_chance, mutation_chance)
            pop_builder.eval(ft.QuadError(), self._dataset)
            pop_builder.select_fittest()


def usage():
    print 'example: main.py -d dataset.txt -c config.properties' \
          '\n --dataset_file=dataset.txt --config=config.properties'
    sys.exit(2)


def main():
    dataset_file = ""
    config = ""
    try:
        arg_list = sys.argv[1:]
        opts, args = getopt.getopt(arg_list, 'd:c:h', ['dataset_file=', 'config=', 'help'])
    except getopt.GetoptError:
        usage()

    for opt, arg in opts:
        if opt == '-h':
            usage()
        elif opt in ("-d", "--dataset_file"):
            dataset_file = arg
            print arg
        elif opt in ("-c", "--config="):
            config = arg
            print arg
    MultiVariableRegression(dataset_file, config)


if __name__ == "__main__":
    main()
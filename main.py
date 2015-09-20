#!/bin/python
__author__ = 'Waner Miranda'
import numpy as np
import sys
import getopt


class MultiVariableRegression:
    def __init__(self, dataset):
        """

        :type dataset: unicode
        """
        self._dataset = []
        for line in open(dataset):
            value_line = []
            for value in line.rstrip('\n\r').replace('  ', ' ').split(' '):
                if value.strip(' ').__len__() != 0:
                    value_line.append(float(value))
            if value_line:
                self._dataset.append(value_line)
        self._dataset = np.array(self._dataset)
        print self._dataset.shape
        r, c = self._dataset.shape[:2]
        if c == 3:
            self._dataset = self._dataset[:, 1:]
        print self._dataset


def usage():
    print 'example: main.py -f dataset.txt' \
          '\n --dataset_file: dataset.txt'
    sys.exit(2)


def main():
    dataset_file = ""
    try:
        arg_list = sys.argv[1:]
        opts, args = getopt.getopt(arg_list, 'd:h', ['dataset_file=', 'help'])
    except getopt.GetoptError:
        usage()

    for opt, arg in opts:
        if opt == '-h':
            usage()
        elif opt in ("-d", "--dataset_file"):
            dataset_file = arg
            print arg
    MultiVariableRegression(dataset_file)


if __name__ == "__main__":
    main()
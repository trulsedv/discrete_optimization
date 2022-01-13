#!/usr/bin/python
# -*- coding: utf-8 -*-

import knapsack
from collections import namedtuple
Item = namedtuple("Item", ['index', 'value', 'weight', 'density'])


def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    firstLine = lines[0].split()
    item_count = int(firstLine[0])
    capacity = int(firstLine[1])

    items = []

    for i in range(1, item_count + 1):
        line = lines[i]
        parts = line.split()
        items.append(Item(i - 1,
                          int(parts[0]),
                          int(parts[1]),
                          int(parts[0]) / int(parts[1])))

    # solve_it
    output_data = knapsack.DFS_iterative(items, item_count, capacity)
    # output_data = knapsack.dynamic_programing(items, item_count, capacity)

    return output_data


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  '
              + 'Please select one from the data directory.'
              + ' (i.e. python solver.py ./data/ks_4_0)')

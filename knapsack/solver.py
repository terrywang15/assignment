#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple
from itertools import compress
from operator import itemgetter


Item = namedtuple("Item", ['index', 'value', 'weight'])


def enough_space(cur_sel, items, capacity):
    """
    Check current selection against weight constraint
    :param cur_sel:
    :param capacity:
    :return:
    """
    cur_sel_bool = list(map(bool, cur_sel))
    sel_items = list(compress(items, cur_sel_bool))

    return sum([i[2] for i in sel_items]) <= capacity


def optimistic_eval(cur_sel, items, capacity):
    """
    Evaluate objective function with linear relaxation
    :param cur_sel:
    :param items:
    :param capacity:
    :return:
    """
    if len(cur_sel) < len(items):
        cur_sel_bool = list(map(bool, cur_sel))
        sel_items = list(compress(items, cur_sel_bool))
        downstream_sel = items[len(cur_sel_bool):]
        # sort downstream items by value/weight to make sure optimistic eval yields highest possible value
        downstream_sel = sorted(downstream_sel, key=lambda x: x[1]/x[2], reverse=True)

        val = sum([item[1] for item in sel_items])
        wgt = sum([item[2] for item in sel_items])

        capacity_left = capacity - wgt

        for itm in downstream_sel:
            cap_ratio = capacity_left / itm[2]
            if cap_ratio < 1:
                val += cap_ratio * itm[1]
                break
            else:
                val += itm[1]
                wgt += itm[2]
                capacity_left -= wgt
        return val

    else:
        cur_sel_bool = list(map(bool, cur_sel))
        sel_items = list(compress(items, cur_sel_bool))
        # at the bottom of tree, calculate actual value (without linear relaxation)
        total_val = sum([itm[1] for itm in sel_items])
        return total_val

def solve_it(input_data):
    """

    :param input_data:
    :return:
    """
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    firstLine = lines[0].split()
    item_count = int(firstLine[0])
    capacity = int(firstLine[1])

    items = []

    for i in range(1, item_count+1):
        line = lines[i]
        parts = line.split()
        items.append(Item(i-1, int(parts[0]), int(parts[1])))

    # run optimistic eval on each step
    picked = []
    optimized = 0
    # initiate frontier with two choices
    frontier = []
    for choice in [[0], [1]]:
        if enough_space(choice, items, capacity):
            frontier.append((choice, optimistic_eval(choice, items, capacity)))
    curr_best_optim = 0
    while True:
        best_idx, best_val = max(enumerate(frontier), key=lambda x:x[1][1])
        # remove best choice and add the next steps
        best_choice = frontier[best_idx][0]
        # if best choice also has the len == item_count
        # then break and optimized solution is found
        if len(best_choice) == item_count:
            picked = best_choice
            curr_best_optim = sum([i[1] for i in list(compress(items, list(map(bool,picked))))])
            optimized = 1
            break
        del frontier[best_idx]
        for choice in [best_choice + [0], best_choice + [1]]:
            if enough_space(choice, items, capacity):
                frontier.append((choice, optimistic_eval(choice, items, capacity)))

    # translate picked items to the right format
    # Since we are using the heuristics approach, this will not be "optimized values"
    output = str(curr_best_optim) + ' ' + optimized + '\n'
    output += ' '.join([str(i) for i in picked])

    return output


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)')

#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple
from copy import deepcopy
from datetime import datetime, timedelta
from itertools import compress


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
        val = sum([item[1] for item in sel_items])
        capacity_left = capacity - sum([item[2] for item in sel_items])
        for itm in downstream_sel:
            if capacity_left < itm[2]:
                cap_ratio = capacity_left / itm[2]
                val += cap_ratio * itm[1]
                break
            else:
                val += itm[1]
                capacity_left = capacity_left - itm[2]
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
    # sort items by v/w to save on computation
    items = sorted(items, key=lambda x: x[1]/x[2], reverse=True)
    # initiate frontier with two choices
    frontier = []
    for choice in [[0], [1]]:
        if enough_space(choice, items, capacity):
            frontier.append((choice, optimistic_eval(choice, items, capacity)))
    best_choice = []
    curr_best_optim = 0
    # start time counter, when time delta is more than 5 minutes then
    time_limit = timedelta(minutes=5)
    time_elapsed = datetime.now() - datetime.now()
    while True:
        if time_elapsed < time_limit:
            start_time = datetime.now()
            best_idx, best_val = max(enumerate(frontier), key=lambda x:x[1][1])
            # remove best choice and add the next steps
            best_choice = frontier[best_idx][0]
            # if best choice also has the len == item_count
            # then break and optimized solution is found
            if len(best_choice) == item_count:
                itm_idx = [i[0] for i in items]
                picked = [i[1] for i in sorted(zip(itm_idx, best_choice), key=lambda x:x[0])]
                curr_best_optim = sum([i[1] for i in list(compress(items, list(map(bool,best_choice))))])
                optimized = 1
                break
            del frontier[best_idx]
            for choice in [best_choice + [0], best_choice + [1]]:
                if enough_space(choice, items, capacity):
                    frontier.append((choice, optimistic_eval(choice, items, capacity)))
            time_elapsed += datetime.now() - start_time
        else:
            # find best deepest searches i.e. non-optimized solutions
            best_nonoptim = max([i for i in frontier if len(i[0]) == item_count], key=lambda x:x[1])
            solutions = [(list(zip([i[0] for i in items], best_nonoptim[0])), best_nonoptim[1])]
            # get selected and downstream items
            cur_sel_idx = list(zip([i[0] for i in items], best_choice))
            cur_sel_bool = list(map(bool, best_choice))
            sel_items = list(compress(items, cur_sel_bool))
            downstream_sel = items[len(cur_sel_bool):]
            val = sum([item[1] for item in sel_items])
            capacity_left = capacity - sum([item[2] for item in sel_items])
            # fill results using 3 heuristics
            # first heuristic: fill sack by value of items
            heu1_sel = list(zip(cur_sel_idx, best_choice))
            heu1_val = deepcopy(val)
            heu1_cap = deepcopy(capacity_left)
            for itm in sorted(downstream_sel, key=lambda x: x[1], reverse=True):
                if itm[2] <= heu1_cap:
                    heu1_val += itm[1]
                    heu1_cap -= itm[2]
                    heu1_sel.append((itm[0], 1))
                else:
                    heu1_sel.append((itm[0], 0))
            solutions.append((heu1_sel, heu1_val))

            # second heuristic: fill sack by inverse of weight of items
            heu2_sel = list(zip(cur_sel_idx, best_choice))
            heu2_val = deepcopy(val)
            heu2_cap = deepcopy(capacity_left)
            for itm in sorted(downstream_sel, key=lambda x: x[2], reverse=True):
                if itm[2] <= heu1_cap:
                    heu2_val += itm[1]
                    heu2_cap -= itm[2]
                    heu2_sel.append((itm[0], 1))
                else:
                    heu2_sel.append((itm[0], 0))
            solutions.append((heu2_sel, heu2_val))

            # third heuristic: fill sack by value over weight
            heu3_sel = list(zip(cur_sel_idx, best_choice))
            heu3_val = deepcopy(val)
            heu3_cap = deepcopy(capacity_left)
            for itm in items:
                if itm[2] <= heu1_cap:
                    heu3_val += itm[1]
                    heu3_cap -= itm[2]
                    heu3_sel.append((itm[0], 1))
                else:
                    heu3_sel.append((itm[0], 0))
            solutions.append((heu3_sel, heu3_val))

            # get max of the solutions
            best_heu = max(solutions, key=lambda x: x[1])
            picked = [i[1] for i in sorted(best_heu[0], key=lambda x: x[0])]
            curr_best_optim = best_heu[1]
            break

    # translate picked items to the right format
    # Since we are using the heuristics approach, this will not be "optimized values"
    output = str(curr_best_optim) + ' ' + str(optimized) + '\n'
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

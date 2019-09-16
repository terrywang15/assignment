#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple


Item = namedtuple("Item", ['index', 'value', 'weight'])


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

    # print(capacity)

    items = []

    for i in range(1, item_count+1):
        line = lines[i]
        parts = line.split()
        items.append(Item(i-1, int(parts[0]), int(parts[1])))

    # print(items)

    # sort items by value/weight, highest first
    # then sort again by weight so we fill by smallest weight first
    # items_sorted = set(sorted(items, key=lambda x: x[1] / x[2], reverse=True))
    items_sorted = set(sorted(items, key=lambda x: x[2], reverse=False))
    # print(items_sorted)


















    # fill items using item_sorted up to capacity
    # Run this 10 times, each time removing items already selected
    num_iter = 0
    picked = set()
    tot_wgt = 0
    tot_val = 0
    while num_iter <=10:
        items_left = items_sorted - picked
        for item in items_left:
            if tot_wgt + item[2] <= capacity:
                picked.add(item)
                tot_val += item[1]
                tot_wgt += item[2]
            else:
                continue
        num_iter += 1

    picked_idx = [i[0] for i in picked]

    # print(picked)

    # translate picked items to the right format
    # Since we are using the heuristics approach, this will not be "optimized values"
    output = str(tot_val) + ' ' + '0' + '\n'
    output += ' '.join(['1' if i[0] in picked_idx else '0' for i in items])

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

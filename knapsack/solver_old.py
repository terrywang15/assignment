#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple


def parse_input(file_location):
    with open(file_location, 'r') as input_data_file:
        input_data = input_data_file.read()

    Item = namedtuple("Item", ['index', 'value', 'weight'])
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

    return items, capacity


class Node:

    def __init__(self, depth, choice, val, weight):
        """
        depth is how deep the node is in the tree structure
        choices is either 1 (chosen) or 0 (not chosen)
        """
        self.id = str(depth) + str(choice)
        self.val = val
        self.weight = weight
        self.depth = depth
        self.choice = choice
        self.children = []
        self.parent = []
        self.path = []

    def add_children(self, other_node):
        self.children.append(other_node)

    def add_parent(self, other_node):
        self.parent.append(other_node)

    def get_children(self):
        return self.children

    def get_parent_id(self):
        if len(self.parent) == 0:
            pass
        else:
            return [n.id for n in self.parent]

    def get_path(self):
        path = []
        cur_node = self
        while cur_node is not None:
            path.insert(0, cur_node.id)
            cur_node = cur_node.parent

        return path


def populate_nodes(items):

    yes_nodes = [Node(idx, 1, val, weight) for idx, val, weight in items]
    no_nodes = [Node(idx, 0, val, weight) for idx, val, weight in items]

    # root note denoted by -1-1
    root_node = Node(-1, -1, 0, 0)
    root_node.add_children(yes_nodes[0])
    root_node.add_children(no_nodes[0])
    all_nodes = [root_node]

    # Nodes have to be sorted by their index

    for idx, node in enumerate(yes_nodes):
        if idx == 0:
            node.add_parent(root_node)
        else:
            node.add_parent(yes_nodes[idx-1])
            node.add_parent(no_nodes[idx-1])
        if idx == len(yes_nodes)-1:
            pass
        else:
            node.add_children(yes_nodes[idx+1])
            node.add_children(no_nodes[idx+1])
        all_nodes.append(node)

    for idx, node in enumerate(no_nodes):
        if idx == 0:
            node.add_parent(root_node)
        else:
            node.add_parent(yes_nodes[idx-1])
            node.add_parent(no_nodes[idx-1])
        if idx == len(yes_nodes)-1:
            pass
        else:
            node.add_children(yes_nodes[idx+1])
            node.add_children(no_nodes[idx+1])
        all_nodes.append(node)

    return all_nodes


def find_node(all_nodes, depth, choice):
    """
    find index of node given id
    """
    idx = str(depth) + str(choice)
    return all_nodes[[n.id for n in all_nodes].index(idx)]


def back_to_last_left(path):
    """
    find where is the last step where choice is 1:
    reverse the index of choices, grab index of first 1, add 1, add minus sign,
    gives you index of the last 1
    """
    return path[:-([n.choice for n in path][::-1].index(1))]


def calculate_score(path, max_weight):
    """
    returns objective function given path
    """
    # check if total weight > weight constraint

    if sum([n.weight*n.choice for n in path]) > max_weight:
        return -1000000

    return sum([n.val*n.choice for n in path])


def traverse_tree_stupid(all_nodes, capacity=10):
    """
    traverses the tree in a depth first search manner, exhaust all solutions,
    and returns list of solutions
    """
    # root has to be the first node
    cur_node = all_nodes[0]
#     visited = set([cur_node])
    path = [cur_node]
    solutions = []

#     while not solved or len_solutions == 2**((len(all_nodes)-1)/2):
    while True:
        # if reached the deepest layer and is in the left branch,
        # go up to the last step in path where the step's choice is 1,
        # and go to the node with the same depth but choice 0
        # print("currently at " + cur_node.id)
        if path[-1].depth+1 == (len(all_nodes)-1)/2:
            # currently at left branch, go to right branch
            if path[-1].choice == 1:
                # print("at bottom left")
                solutions.append(([n.id for n in path], calculate_score(path, capacity)))
                # remove last step in path
                cur_node = find_node(all_nodes, path[-1].depth, 0)
                path = path[:-1]
                path.append(cur_node)
                # print('going to the right')
            elif path[-1].choice == 0:
                # find where is the last step where choice is 1:
                # reverse the index of choices,
                # grab index of first 1, add 1, add minus sign,
                # gives you index of the last 1
                # print("at bottom right")
                # make calculations
                solutions.append(([n.id for n in path], calculate_score(path, capacity)))

                # try skipping back to lowest depth where choice is 1
                # If can't find it it means that you have to
                # print("trying to go back up")
                try:
                    path = back_to_last_left(path)
                    cur_node = find_node(all_nodes, path[-1].depth, 0)
                    path = path[:-1]
                    path.append(cur_node)
                except:
                    # exhausted solutions if all nodes in the deepest layer are visited
                    break
        else:
            # Go one layer deeper to the left
            cur_node = find_node(all_nodes, path[-1].depth+1, 1)
            path.append(cur_node)
            # print("going one layer deeper to " + cur_node.id)

    # get the solution with the highest calculate_score
    best_solution = sorted(solutions, key=lambda x: x[1], reverse=True)[0]

    # return solutions
    return best_solution

def space_left():
    pass


def optimistic_value():
    pass


def traverse_tree_optim(all_nodes, capacity=10):
    """
    Traverse tree with optimized node search using linear relaxation
    :param all_nodes:
    :param capacity:
    :return:
    """




def write_output(best_solution):
    """
    Parses best_solution's path and returns desired strings
    """
    output_data = str(best_solution[1]) + ' ' + str(1) + '\n'
    output_data += ' '.join([i[1] for i in best_solution[0] if int(i[1]) != -1])

    return output_data


def solve_it(items, capacity):
    # Modify this code to run your optimization algorithm
    # populate nodes into searchable tree
    all_nodes = populate_nodes(items)

    # Traverse tree to find best solution
    best_solution = traverse_tree_stupid(all_nodes, capacity=capacity)

    # prepare the solution in the specified output format
    return write_output(best_solution)


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



if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        items, capacity = parse_input(file_location)

        # solve the problem
        print(solve_it(items, capacity))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)')

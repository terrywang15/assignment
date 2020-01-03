#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys

x = 100000
sys.setrecursionlimit(x)


def solve_it(input_data):

    # parse the input
    lines = input_data.split('\n')

    first_line = lines[0].split()
    node_count = int(first_line[0])
    edge_count = int(first_line[1])

    edges = []
    for i in range(1, edge_count + 1):
        line = lines[i]
        parts = line.split()
        edges.append((int(parts[0]), int(parts[1])))

    output = {}
    forbidden_colors = {}

    # This part is for constraint - consider expanding
    def is_safe(node_id, color_id):
        """
        Check if node with the given color is valid
        :param node_id: int
        :param color_id: int
        :return: boolean
        """
        for idx in range(node_count):
            if (node_id, idx) in edges or (idx, node_id) in edges:
                try:
                    if color_id == output[idx] or color_id in forbidden_colors[node_id]:
                        return False
                except:
                    continue
        return True

    # Backtrack solution
    def color_graph(node_idx):
        """
        Recursively try coloring nodes down the line basically like a tree search with constraints updated
        depth first search
        I think this works, but too much recursion seems to lead to crashes
        :param node_idx: integer node index
        :return: dict of integer where index is node and content is the color index
        """
        assert node_idx >= 0
        # create empty list for forbidden colors memory
        if node_idx not in forbidden_colors:
            forbidden_colors[node_idx] = []
        # here we need to define how many colors to try
        # I know the ceiling is len(nodes) but unsure about the floor - can update this part
        # n_colors = node_count
        n_colors = 5
        valid_assn = False
        for color in range(n_colors):
            # print("trying color " + str(color))
            if is_safe(node_idx, color):
                output[node_idx] = color
                valid_assn = True
                print("assigned color " + str(color) + " to node " + str(node_idx))
                break
        if valid_assn:
            if (node_idx + 1) < node_count:
                color_graph(node_idx+1)
            else:
                print("complete")
        elif (node_idx - 1) >= 0:
            print("backtracking")
            # clear downstream backtrack memory
            forbidden_colors[node_idx] = []
            # add color to forbidden colors dict
            forbidden_colors[node_idx-1].append(output[node_idx-1])
            # remove the dict entry for that color
            del output[node_idx - 1]
            # backtrack
            color_graph(node_idx-1)
        else:
            print("unable to find a solution")

    color_graph(0)
    solution, optimal = list(output.values()), str(0)

    # prepare the solution in the specified output format
    output_data = str(node_count) + ' ' + optimal + '\n'
    output_data += ' '.join(map(str, solution))

    return output_data


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/gc_4_1)')


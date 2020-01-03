#!/usr/bin/python
# -*- coding: utf-8 -*-
import networkx as nx
import numpy as np


class SolutionNotFound(Exception):
    pass


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

    # create matrix to keep track of current constraints


    # make networkx graph with edgelist
    edges_nx = []
    for i in range(1, edge_count + 1):
        line = lines[i]
        parts = line.split()
        edges_nx.append(parts[0] + " " + parts[1])

    g = nx.read_edgelist(edges_nx)

    # find how many nodes are in the largest clique - this gives the most optimal solution
    max_colors = max(map(len, nx.find_cliques(g)))

    output = {}

    # This part is for constraint - consider expanding
    def is_safe(node_id, color_id):
        """
        Check if node with the given color is valid
        :param edges: list of tuples
        :param node_id: int
        :param color_id: int
        :param output: dict, current state of things
        :return: boolean
        """
        for idx in range(node_count):
            if (node_id, idx) in edges or (idx, node_id) in edges:
                if idx in output:
                    if color_id == output[idx]:
                        return False
        return True

    # make an iteration with the cliques
    for clique in nx.find_cliques(g):
        for node in clique:
            if node not in output:
                color_assn = False
                # Node not in output, assign a color from range(max_colors)
                for color in range(max_colors):
                    if is_safe(node, color):
                        output[node] = color
                        color_assn = True
                    if not color_assn:
                        raise SolutionNotFound









    # Backtrack solution with while loop
    def color_graph(edges, node_count, max_colors):
        """
        solves a coloring problem given the list of edges and node count
        super slow, but will give the optimal solution
        :param edges: list of tuples
        :param node_count: int
        :param max_colors: int
        :return: dict with node id as key and color id as value
        """

        forbidden_colors = {}
        output = {}
        cur_node = 0
        solution_found = False

        while not solution_found:
            valid_assn = False
            # print("curretly at node " + str(cur_node))
            if cur_node < 0:
                print("Exhausted all solutions, unable to solve with max_colors = " + str(max_colors))
                raise SolutionNotFound
            # create empty set for forbidden colors memory
            if cur_node not in forbidden_colors:
                forbidden_colors[cur_node] = set()
            # at each node, try all colors minus forbidden colors:
            valid_colors = set(range(max_colors)) - forbidden_colors[cur_node]
            for color in valid_colors:
                if not valid_assn and is_safe(cur_node, color, edges, output):
                    # print("trying color " + str(color))
                    output[cur_node] = color
                    valid_assn = True
                    # print("assigned color " + str(color) + " to node " + str(cur_node))
            if valid_assn:
                if (cur_node + 1) < node_count:
                    cur_node += 1
                    continue
                else:
                    # print("Solution found")
                    return output
            elif (cur_node - 1) >= 0:
                # print("backtracking")
                # clear downstream backtrack memory
                forbidden_colors[cur_node] = set()
                # add color to forbidden colors dict
                forbidden_colors[cur_node - 1].add(output[cur_node - 1])
                # remove the dict entry for that color
                del output[cur_node - 1]
                # backtrack
                cur_node -= 1
            else:
                print("Exhausted all solutions, unable to solve with max_colors = " + str(max_colors))
                raise SolutionNotFound

    output = color_graph(edges, node_count, max_colors)
    solution, optimal = list(output.values()), "1"

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


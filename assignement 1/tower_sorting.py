#!/usr/bin/env python
"""
Name of the author(s):
- Auguste Burlats <auguste.burlats@uclouvain.be>
"""
import time
import sys
import copy

from copy import deepcopy
from search import *


#################
# Problem class #
#################
class TowerSorting(Problem):

    def actions(self, state):
        dest = []
        actions = []
        for i in range(0, len(state.grid)):
            if len(state.grid[i]) != state.size:
                dest.append(i)
        for i in range(0, len(state.grid)):
            for j in range(0, len(dest)):
                if i != j and len(state.grid[i]) > 0:
                    actions.append((i, dest[j]))
        return actions
    

    def result(self, state, action):
        test = copy.deepcopy(state)
        test.grid[action[1]].append(test.grid[action[0]].pop())
        return test

    def goal_test(self, state):
        for i in range(0, len(state.grid)):
            if len(state.grid[i]) == 0:
                pass
            else:
                colour = state.grid[i][0]
                for j in range (0, len(state.grid[i])):
                    if colour != state.grid[i][j] or len(state.grid[i]) != state.size:
                        return False
        return True
        

###############
# State class #
###############
class State:

    def __init__(self, number, size, grid, move="Init"):
        self.number = number
        self.size = size
        self.grid = grid
        self.move = move

    def __str__(self):
        s = self.move + "\n"
        for i in reversed(range(self.size)):
            for tower in self.grid:
                if len(tower) > i:
                    s += "".join(tower[i]) + " "
                else:
                    s += ". "
            s += "\n"
        return s

    def __eq__(self, other):
        if isinstance(other, State) and hash(self) == hash(other):
            return True
        else:
            return False

    def __hash__(self):
        """
        basis = 1
        hashed = 0
        for i in self.grid:
            for j in i:
                if j:
                    hashed+= basis
                basis *= 2

        return hash(hashed)
        """
        return hash(tuple(map(tuple, self.grid)))

######################
# Auxiliary function #
######################
def read_instance_file(filepath):
    with open(filepath) as fd:
        lines = fd.read().splitlines()

    number_tower, size_tower = tuple([int(i) for i in lines[0].split(" ")])
    initial_grid = [[] for i in range(number_tower)]
    for row in lines[1:size_tower+1]:
        elems = row.split(" ")
        for index in range(number_tower):
            if elems[index] != '.':
                initial_grid[index].append(elems[index])

    for tower in initial_grid:
        tower.reverse()

    return number_tower, size_tower, initial_grid


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: ./sort_tower.py <path_to_instance_file>")
    filepath = sys.argv[1]

    number, size, initial_grid = read_instance_file(filepath)

    init_state = State(number, size, initial_grid, "Init")
    problem = TowerSorting(init_state)
    # Example of search
    start_timer = time.perf_counter()
    node, nb_explored, remaining_nodes = breadth_first_graph_search(problem)
    end_timer = time.perf_counter()

    # Example of print
    path = node.path()

    for n in path:
        # assuming that the __str__ function of state outputs the correct format
        print(n.state)

    print("* Execution time:\t", str(end_timer - start_timer))
    print("* Path cost to goal:\t", node.depth, "moves")
    print("* #Nodes explored:\t", nb_explored)
    print("* Queue size at goal:\t",  remaining_nodes)

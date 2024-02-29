#! /usr/bin/env python3
"""NAMES OF THE AUTHOR(S): Auguste Burlats <auguste.burlats@uclouvain.be>"""
from search import *
import copy
from random import randrange

class AtomPlacement(Problem):

    # if you want you can implement this method and use it in the maxvalue and randomized_maxvalue functions
    def successor(self, state):
        def swap(state, i, j):
            temp = state.sites[i]
            state.sites[i] = state.sites[j]
            state.sites[j] = temp
            return state
        successors = []
        for i in range(len(state.sites)):
            for j in range(i, len(state.sites)):
                test = copy.deepcopy(state)
                test = swap(test, i, j)
                successors.append(test)     
        return successors
                
                
            

    # if you want you can implement this method and use it in the maxvalue and randomized_maxvalue functions
    def value(self, state):
        energy = 0
        for i in range(len(state.sites)):
            for edge in state.edges:
                if i in edge:
                    M = state.sites[edge[0]]
                    N = state.sites[edge[1]]
                    energy += state.energy_matrix[M][N]
        return energy


class State:

    def __init__(self, n_sites, n_types, edges, energy_matrix, sites=None):
        self.k = len(n_types)
        self.n_types = n_types
        self.n_sites = n_sites
        self.n_edges = len(edges)
        self.edges = edges
        self.energy_matrix = energy_matrix
        if sites is None:
            self.sites = self.build_init()
        else:
            self.sites = sites

    # an init state building is provided here but you can change it at will
    def build_init(self):
        sites = []
        for atom_type, quantity in enumerate(self.n_types):
            for i in range(quantity):
                sites.append(atom_type)

        return sites

    def __str__(self):
        s = ''
        for v in self.sites:
            s += ' ' + str(v)
        return s


def read_instance(instanceFile):
    file = open(instanceFile)
    line = file.readline()
    #nombre de nodes/places
    n_sites = int(line.split(' ')[0])
    #nombre de type
    k = int(line.split(' ')[1])
    #nombre d'edges
    n_edges = int(line.split(' ')[2])
    #matrice d'edges entre les position
    edges = []
    file.readline()
    #nombre de chaque type
    n_types = [int(val) for val in file.readline().split(' ')]
    if sum(n_types) != n_sites:
        print('Invalid instance, wrong number of sites')
    file.readline()
    #interaction différent type
    energy_matrix = []
    for i in range(k):
        energy_matrix.append([int(val) for val in file.readline().split(' ')])
    file.readline()

    for i in range(n_edges):
        edges.append([int(val) for val in file.readline().split(' ')])

    return n_sites, n_types, edges, energy_matrix


# Attention : Depending of the objective function you use, your goal can be to maximize or to minimize it
def maxvalue(problem, limit=100):
    current = LSNode(problem, problem.initial, 0)
    best = current
    for step in range(limit):
        successors = problem.successor(problem)
        successors.sort(key = problem.value)
        current = successors[0]
        if current.value(current) > best.value(best):
            best = current
    # Put your code here

    return best


# Attention : Depending of the objective function you use, your goal can be to maximize or to minimize it
def randomized_maxvalue(problem, limit=100):
    current = LSNode(problem, problem.initial, 0)
    best = current
    for step in range(limit):
        successors = problem.successor(problem)
        successors.sort(key = problem.value)
        current = successors[randrange(5)]
        if current.value(current) > best.value(best):
            best = current
    # Put your code here

    return best


#####################
#       Launch      #
#####################
if __name__ == '__main__':
    info = read_instance(sys.argv[1])
    init_state = State(info[0], info[1], info[2], info[3])
    ap_problem = AtomPlacement(init_state)
    step_limit = 100
    node = maxvalue(ap_problem, step_limit)
    state = node.state
    print(state)

from search import *
import copy
import time

#################
# Problem class #
#################

class SoftFlow(Problem):

    def __init__(self, initial):
        self.initial = initial
        self.letters = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j')
        self.numbers = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9')
        self.goal = []
        for h in range(0, len(self.letters)):
            for i in range(0, len(initial.grid)):
                if self.letters[h] in initial.grid[i]:
                    self.initial.entry.append((i, initial.grid[i].index(self.letters[h])))
                if self.numbers[h] in initial.grid[i]:
                    initial.out.append((i, initial.grid[i].index(self.numbers[h])))
                
            if len(self.initial.entry) < h+1:
                break
        
        
    def actions(self, state):
        action = []
        i = 0
        while i in range(0, len(self.initial.entry)):
            if i in self.goal:
                i += 1
                
            else :
                if state.entry[i] != state.out[i]:
                    if i!= 0 and state.entry[i-1] != state.out[i-1]:
                        return action
                    if state.grid[state.entry[i][0]+1][state.entry[i][1]] == ' ' or (state.entry[i][0]+1, state.entry[i][1]) == state.out[i]:
                        action.append((i, (state.entry[i][0]+1, state.entry[i][1])))
                    if state.grid[state.entry[i][0]-1][state.entry[i][1]] == ' ' or (state.entry[i][0]-1, state.entry[i][1]) == state.out[i]:
                        action.append((i, (state.entry[i][0]-1, state.entry[i][1])))
                    if state.grid[state.entry[i][0]][state.entry[i][1] -1] == ' ' or (state.entry[i][0], state.entry[i][1]-1) == state.out[i]:
                        action.append((i, (state.entry[i][0], state.entry[i][1]-1)))
                    if state.grid[state.entry[i][0]][state.entry[i][1] +1] == ' ' or (state.entry[i][0], state.entry[i][1]+1) == state.out[i]:
                        action.append((i, (state.entry[i][0], state.entry[i][1]+1)))
                    return action
        return action
            

    def result(self, state, action):
        test = copy.deepcopy(state)
        test.grid[test.entry[action[0]][0]][test.entry[action[0]][1]] = self.numbers[action[0]]
        x = state.out[action[0]]
        if x == (action[1][0] +1, action[1][1]) or x == (action[1][0] -1, action[1][1]) or x == (action[1][0], action[1][1] +1)  or x == (action[1][0], action[1][1] -1) :
            test.grid[action[1][0]][action[1][1]] = self.numbers[action[0]]
            test.entry[action[0]] = x
            self.goal.append(action[0])
            return test
        else:
            test.grid[action[1][0]][action[1][1]] = self.letters[action[0]]
            test.entry[action[0]] = action[1]
        return test


    def goal_test(self, state):
        for i in range(0, len(state.entry)):
            if state.entry[i] != state.out[i]:
                return False
        return True
    
    def h(self, node):
        if node.action == None:
            h = 0
        else:
            
            h = 0
            for i in range(0, len(node.state.entry)):
                h += abs((node.state.entry[i][0] - node.state.out[i][0]) + (node.state.entry[i][1] - node.state.out[i][1]))
        # ...
        # compute an heuristic value
        # ...
        return h
        

    def load(path):
        with open(path, 'r') as f:
            lines = f.readlines()
            
        state = State.from_string(''.join(lines))
        return SoftFlow(state)



###############
# State class #
###############

class State:

    def __init__(self, grid):
        self.nbr = len(grid)
        self.nbc = len(grid[0])
        self.grid = grid
        self.entry = []
        self.out = []
        
    def __str__(self):
        return '\n'.join(''.join(row) for row in self.grid)

    def __eq__(self, other_state):
        if isinstance(other_state, State) and hash(self) == hash(other_state):
            return True
        else:
            return False

    def __hash__(self):
        return hash(tuple(map(tuple, self.grid)))
    
    def __lt__(self, other):
        return hash(self) < hash(other)

    def from_string(string):
        lines = string.strip().splitlines()
        return State(list(
            map(lambda x: list(x.strip()), lines)
        ))






#####################
# Launch the search #
#####################

problem = SoftFlow.load(sys.argv[1])
node = astar_search(problem)

# example of print
path = node.path()

print('Number of moves: ', str(node.depth))
for n in path:
    print(n.state)  # assuming that the _str_ function of state outputs the correct format
    print()
import numpy as np
from enum import Enum

class Coord():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Coord(self.x + other.x, self.y + other.y)
    def __repr__(self):
        return "({}, {})".format(self.x, self.y)

    def __eq__(self, other):
        if type(other) is type(self):
            return self.x == other.x and self.y == other.y  

    def __sub__(self, other):

        return Coord(self.x - other.x, self.y - other.y)  
    def __hash__(self):
        """Overrides the default implementation"""
        return hash((self.x, self.y))
    

class Grid():
    def __init__(self, moves=None, shape=(8,8), chain_length=2):
        self.moves = moves
        self.shape = shape
        self.head = Node(0, Coord(0,0), self)
        prev_node = self.head
        
        for i in range(1, chain_length):
            curr_node = Node(i, Coord(0,0), self)
            prev_node.next_node = curr_node
            curr_node.prev_node = prev_node
            prev_node = curr_node
        self.tail = curr_node

        self.visited = set()
        self.visited.add(self.tail.position)

    def execute_moves(self, moves):
        if moves is not None:
            for move in moves:
                self.head.execute_move(move)

    def __repr__(self):
        repr_string = ""
        values = np.full(self.shape, ".", np.unicode_)
        if self.tail is None:
            repr_string = "Empty chain."
        else:
            current_node = self.tail
            while current_node is not None:
                values[current_node.position.x, current_node.position.y] = current_node.id
                current_node = current_node.prev_node
            for c in values:
                for v in c:
                    repr_string += str(v)
                repr_string += "\n"
        return repr_string

    def get_visited_grid(self):
        if self.visited is not None:
            visited_array = np.full(self.shape, ".", np.unicode_)
            for v in self.visited:
                visited_array[v.x, v.y] = "#"
            return visited_array
            

class Node():
    def __init__(self, id, position, grid=None, next_node=None, prev_node=None):
        self.id = id
        self.position = position
        self.next_node = next_node
        self.prev_node = prev_node
        self.grid = grid

    def execute_move(self, move):
        for u in range(move.units):
            #print("move: {}".format(move))
            self.position += Coord(move.direction[0], move.direction[1])
            if self.next_node is not None:
                diff = self.position - self.next_node.position

                diff_x = diff.x
                diff_y = diff.y

                next_move_direction = np.array([0, 0])

                if abs(diff_x) == 2:
                    next_move_direction[0] = np.sign(diff_x)
                if abs(diff_y) == 2:
                    next_move_direction[1] = np.sign(diff_y)
                if abs(diff_x) + abs(diff_y) == 3:
                    next_move_direction[0] = np.sign(diff_x)
                    next_move_direction[1] = np.sign(diff_y)

                next_node_move = Move(next_move_direction, 1)
                
                self.next_node.execute_move(next_node_move)
            else:
                # its the last node in chain, hence we update visited
                self.grid.visited.add(self.position)
            print("move:  {}".format(move))
            print(self.grid)
            #print(self.grid.get_visited_grid())
            #print(self.grid.visited)
    def __repr__(self):
        return "{}, {}".format(self.id, self.position)

class Move():
    def __init__(self, direction, units):
        self.direction = direction
        self.units = units

    def __repr__(self):
        return "{}, {}".format(self.direction, self.units)


class MoveDirection(Enum): # using this enum for easy parsing below
    U = [1, 0]
    D = [-1, 0]
    R = [0, 1]
    L = [0, -1]

def parse_input(input_file):
    moves = []
    for line in input_file:
        line_split = line.rstrip().split(" ")
        if line_split[0] in ["U", "D", "L", "R"] and str.isnumeric(line_split[1]):
            direction = MoveDirection[line_split[0]] # here we use the enum for easy parsing
            units = int(line_split[1])
            move = Move(direction.value, units)
            moves.append(move)
    return moves


def first_part(moves):
    grid = Grid(shape=(30,30), chain_length=9)
    grid.execute_moves(moves)
    visited = grid.get_visited_grid()
    
    #print(np.flipud(visited))
    return len(grid.visited)

def second_part(moves):
    return None

input_file_name = "2022_python/day09/day09_test.txt"

with open(input_file_name) as input_file:
    moves = parse_input(input_file)
    result_first = first_part(moves)
    print("Result of the first part is: {}".format(result_first))

with open(input_file_name) as input_file:
    moves = parse_input(input_file)
    result_second = second_part(moves)
    print("Result of the second part is: {}".format(result_second))

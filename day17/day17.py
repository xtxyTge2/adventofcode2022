import numpy as np

def parse_input(input_file):
    return input_file.read()

def spawn_new_block(grid, iteration):
    height = get_height(grid)
    empty_row = [[0, 0, 0, 0, 0, 0, 0]]
    for i in range(3):
        grid = np.append(grid, empty_row, axis=0)
        height += 1

    block_positions = []
    if iteration % 5 == 0:
        # block: 
        #       S###
        block_height = 1
        height += block_height
        block_positions.append((height, 2))
        block_positions.append((height, 3))
        block_positions.append((height, 4))
        block_positions.append((height, 5))
    elif iteration % 5 == 1:
        block_height = 3
        height += block_height
        block_positions.append((height, 3))
        block_positions.append((height - 1, 2))
        block_positions.append((height - 1, 3))
        block_positions.append((height - 1, 4))
        block_positions.append((height - 2, 3))
        # block:  
        #         .S.
        #         ###
        #         .#.
    
    elif iteration % 5 == 2:
        block_height = 3
        height += block_height
        block_positions.append((height, 4))
        block_positions.append((height - 1, 4))
        block_positions.append((height - 2, 4))
        block_positions.append((height - 2, 3))
        block_positions.append((height - 2, 2))
        # block: 
        #       ..S
        #       ..#
        #       ### 
    elif iteration % 5 == 3:
        block_height = 4
        height += block_height
        block_positions.append((height, 2))
        block_positions.append((height - 1, 2))
        block_positions.append((height - 2, 2))
        block_positions.append((height - 3, 2))
        
        # block:
        #       S
        #       #
        #       #
        #       #
    elif iteration % 5 == 4:
        # block:
        #       S#
        #       ##
        block_height = 2
        height += block_height
        block_positions.append((height, 2))
        block_positions.append((height, 3))
        block_positions.append((height - 1, 2))
        block_positions.append((height - 1, 3))

    for i in range(block_height):
        grid = np.append(grid, empty_row, axis=0)
    for b in block_positions:
        grid[b] = 1

    return (grid, block_positions)


def get_new_block_positions(grid, block_positions, move):
    block_moved = True
    new_block_positions = []
    for b in block_positions:
        if move == "v":
            new_position = (b[0] - 1, b[1])
        elif move == "<":
            new_position = (b[0], b[1] - 1)
        elif move == ">":
            new_position = (b[0], b[1] + 1)
        x, y = new_position[0], new_position[1]
        new_block_positions.append(new_position)
        
        if x < 0 or y < 0 or x > grid.shape[0] - 1 or y > grid.shape[1] - 1:
            block_moved = False
            break
        if grid[new_position] == 2:
            block_moved = False
            break
    if not block_moved:
        new_block_positions = block_positions
    return (block_moved, new_block_positions)

def update_block_positions(grid, old_block_positions, new_block_positions):
    for b in old_block_positions:
        grid[b] = 0
    for b in new_block_positions:
        grid[b] = 1
    return grid

def turn_to_stone(grid, block_positions):
    for b in block_positions:
        grid[b] = 2
    return grid

def move_block(grid, block_positions, move):
    block_moved, new_block_positions = get_new_block_positions(grid, block_positions, move)
    turned_to_stone = False

    if block_moved:
        update_block_positions(grid, block_positions, new_block_positions)
    if not block_moved and move == "v":
        turned_to_stone = True
        turn_to_stone(grid, new_block_positions)
        
    grid = cull_grid_down(grid)
    return (turned_to_stone, grid, new_block_positions)

def cull_grid_down(grid):
    height = get_height(grid)
    grid = grid[:height + 1]
    return grid

def get_height(grid):
    for i in range(grid.shape[0]):
        row_idx = grid.shape[0] - 1 - i
        row = grid[row_idx, :]
        for v in row:
            if v > 0:
                return row_idx
    #return np.argmax(grid > )
def get_height_old(grid):
    for i in range(grid.shape[0]):
        row_idx = grid.shape[0] - 1 - i
        row = grid[row_idx, :]
        for v in row:
            if v > 0:
                return row_idx
    return grid.shape[0] - 1

def get_full_rows_indices(grid):
    full_row = np.array([2, 2, 2, 2, 2, 2, 2])
    full_rows_indices = []
    for i in reversed(range(1, grid.shape[0])):
        row = grid[i, :]
        if np.array_equal(row, full_row):
            full_rows_indices.append(i)
    return full_rows_indices

def run_simulation(moves):
    grid = np.full((1, 7), 0, int)
    grid[-1, :] = 2

    iteration = 0
    move_index = 0
    max_iteration = 2021

    while(iteration <= max_iteration):
        grid, block_position = spawn_new_block(grid, iteration)
        is_falling = False
        turned_to_stone = False
        while not turned_to_stone:
            if is_falling:
                turned_to_stone, grid, block_position = move_block(grid, block_position, "v")
            else:
                move = moves[move_index % len(moves)]
                move_index += 1

                turned_to_stone, grid, block_position = move_block(grid, block_position, move)
            is_falling = not is_falling
        iteration += 1
    return get_height(grid)

def pretty_print(grid):
    grid = np.flipud(grid)
    repr_string = ""
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            v = grid[i, j]
            if v == 2:
                repr_string += "#"
            if v == 0:
                repr_string += "."
            if v == 1:
                repr_string += "@"
        repr_string += "\n"
    print(repr_string)

def first_part(moves):
    height = run_simulation(moves)
    return height

def second_part(data):
    return None


input_file_name = "2022_python/day17/day17.txt"


"""
Test: Result of the first part is: 3068
Real: Result of the first part is: 3109
"""

with open(input_file_name) as input_file:
    data = parse_input(input_file)
    result_first = first_part(data)
    print("Result of the first part is: {}".format(result_first))

with open(input_file_name) as input_file:
    data = parse_input(input_file)
    result_second = second_part(data)
    print("Result of the second part is: {}".format(result_second))
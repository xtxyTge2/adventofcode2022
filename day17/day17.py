import numpy as np


def parse_input(input_file):
    return input_file.read()


class Grid():
    def __init__(self, moves):
        self.grid = np.full((1, 7), 0, int)
        self.grid[-1, :] = 2

        self.current_block_positions = []

        self.moves = moves
        self.move_index = 0

    def _set_next_move(self, move=None):
        if move is None:
            self.current_move = self.moves[self.move_index % len(self.moves)]
            self.move_index += 1
        else:
            self.current_move = "v"

    def _remove_empty_rows_from_top(self):
        height = self.get_height()
        self.grid = self.grid[:height + 1]

    def get_height(self):
        for i in range(self.grid.shape[0]):
            row_idx = self.grid.shape[0] - 1 - i
            row = self.grid[row_idx, :]
            for v in row:
                if v > 0:
                    return row_idx
        return self.grid.shape[0] - 1

    def _spawn_new_block(self, iteration):
        height = self.get_height()
        empty_row = [[0, 0, 0, 0, 0, 0, 0]]
        for i in range(3):
            self.grid = np.append(self.grid, empty_row, axis=0)
            height += 1

        block_positions = []
        if iteration % 5 == 0:
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
        elif iteration % 5 == 2:
            block_height = 3
            height += block_height
            block_positions.append((height, 4))
            block_positions.append((height - 1, 4))
            block_positions.append((height - 2, 4))
            block_positions.append((height - 2, 3))
            block_positions.append((height - 2, 2))
        elif iteration % 5 == 3:
            block_height = 4
            height += block_height
            block_positions.append((height, 2))
            block_positions.append((height - 1, 2))
            block_positions.append((height - 2, 2))
            block_positions.append((height - 3, 2))
        elif iteration % 5 == 4:
            block_height = 2
            height += block_height
            block_positions.append((height, 2))
            block_positions.append((height, 3))
            block_positions.append((height - 1, 2))
            block_positions.append((height - 1, 3))

        for i in range(block_height):
            self.grid = np.append(self.grid, empty_row, axis=0)

        self.current_block_positions = block_positions
        self._set_current_block_value(value=1)

    def _is_valid_block_position(self, block_position):
        x, y = block_position[0], block_position[1]
        if x < 0 or y < 0 or x > self.grid.shape[0] - 1 or y > self.grid.shape[1] - 1:
            return False
        if self.grid[block_position] == 2:
            return False
        return True

    def _set_new_block_positions(self):
        move = self.current_move
        new_block_positions = []
        if move == "v":
            new_block_positions = [(x - 1, y)
                                   for x, y in self.current_block_positions]
        elif move == "<":
            new_block_positions = [(x, y - 1)
                                   for x, y in self.current_block_positions]
        elif move == ">":
            new_block_positions = [(x, y + 1)
                                   for x, y in self.current_block_positions]

        block_moved = True
        for position in new_block_positions:
            if not self._is_valid_block_position(position):
                block_moved = False
                break
        if block_moved:
            # update block positions
            self.current_block_positions = new_block_positions
        return block_moved

    def _set_grid_values(self, positions, value):
        for b in positions:
            self.grid[b] = value

    def _set_current_block_value(self, value):
        self._set_grid_values(
            positions=self.current_block_positions, value=value)

    def _turn_current_block_to_stone(self):
        self._set_current_block_value(value=2)

    def _move_block(self):
        move = self.current_move
        old_block_positions = self.current_block_positions.copy()
        block_moved = self._set_new_block_positions()

        if block_moved:
            # remove old block from grid
            self._set_grid_values(positions=old_block_positions, value=0)
            # add new block to grid
            self._set_grid_values(
                positions=self.current_block_positions, value=1)
        turned_to_stone = False
        if not block_moved and move == "v":
            turned_to_stone = True
            self._turn_current_block_to_stone()
        self._remove_empty_rows_from_top()
        return turned_to_stone

    def _get_full_rows_indices(self):
        full_row = np.array([2, 2, 2, 2, 2, 2, 2])
        full_rows_indices = []
        for i in reversed(range(1, self.grid.shape[0])):
            row = self.grid[i, :]
            if np.array_equal(row, full_row):
                full_rows_indices.append(i)
        return full_rows_indices

    def __repr__(self):
        grid_copy = np.flipud(self.grid.copy())
        repr_string = ""
        for i in range(grid_copy.shape[0]):
            for j in range(grid_copy.shape[1]):
                v = grid_copy[i, j]
                if v == 2:
                    repr_string += "#"
                if v == 0:
                    repr_string += "."
                if v == 1:
                    repr_string += "@"
            repr_string += "\n"
        return repr_string

    def run_simulation(self, total_number_of_blocks):
        current_number_of_blocks = 0
        move_index = 0
        current_grid_state_record = None
        while (current_number_of_blocks <= total_number_of_blocks):
            grid_copy = np.copy(self.grid)

            self._spawn_new_block(current_number_of_blocks)

            history_record = []
            moves_record = []
            is_falling = False
            turned_to_stone = False
            while not turned_to_stone:
                if is_falling:
                    self._set_next_move("v")
                else:
                    self._set_next_move()
                turned_to_stone = self._move_block()
                is_falling = not is_falling
            current_number_of_blocks += 1


def first_part(moves):
    grid = Grid(moves)
    grid.run_simulation(total_number_of_blocks=2021)
    return grid.get_height()


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

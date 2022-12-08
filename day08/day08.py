import numpy as np

def parse_input(input_file):
    tree_map = []
    for line in input_file:
        tree_map.append(list(map(int, line.rstrip())))
    return np.array(tree_map)

def mark_visible_trees_from_left(tree_map):
    position_array = np.zeros(tree_map.shape)
    for i, row in enumerate(tree_map):
        position_array[i, 0] # for the first entry of each row!
        current_max_value = row[0]
        position_array[i, 0] += 1
        for j, v in enumerate(row):
            if v > current_max_value:
                current_max_value = v
                position_array[i, j] += 1
    return position_array

def count_number_of_visible_trees(tree_map):
    shape = tree_map.shape
    position_array_left = mark_visible_trees_from_left(tree_map)
    tree_map = np.rot90(tree_map)
    position_array_top = np.rot90(mark_visible_trees_from_left(tree_map), 3)
    tree_map = np.rot90(tree_map)
    position_array_right = np.rot90(mark_visible_trees_from_left(tree_map), 2)
    tree_map = np.rot90(tree_map)
    position_array_bottom = np.rot90(mark_visible_trees_from_left(tree_map), 1)

    position_array_all_sides = position_array_left + position_array_top \
        + position_array_right + position_array_bottom

    count = 0
    for row in position_array_all_sides:
        for v in row:
            if v >= 1:
                count += 1
    return int(count)

def calculate_scenic_score(tree_map, i, j):
    tree = tree_map[i, j]

    # going left
    left_distance = 0
    for y in range(j - 1, -1, -1):
        other_tree = tree_map[i, y]
        left_distance += 1
        if(other_tree >= tree):
            break
    # going right
    right_distance = 0
    for y in range(j + 1, tree_map.shape[0], 1):
        other_tree = tree_map[i, y]
        right_distance += 1
        if(other_tree >= tree):
            break

    # going top
    top_distance = 0
    for x in range(i - 1, -1, -1):
        other_tree = tree_map[x, j]
        top_distance += 1
        if(other_tree >= tree):
            break

    # going bottom
    bottom_distance = 0
    for x in range(i + 1, tree_map.shape[1], 1):
        other_tree = tree_map[x, j]
        bottom_distance += 1
        if(other_tree >= tree):
            break

    return left_distance * top_distance * right_distance * bottom_distance

def first_part(tree_map):
    return count_number_of_visible_trees(tree_map)

def second_part(tree_map):
    num_rows = tree_map.shape[0]
    num_cols = tree_map.shape[1]

    scenic_scores = np.zeros(tree_map.shape)
    for i in range(num_rows):
        for j in range(num_cols):
            scenic_scores[i, j] = calculate_scenic_score(tree_map, i, j)

    return int(np.max(scenic_scores))

input_file_name = "2022_python/day08/day08.txt"

with open(input_file_name) as input_file:
    tree_map = parse_input(input_file)
    result_first = first_part(tree_map)
    print("Result of the first part is: {}".format(result_first))

with open(input_file_name) as input_file:
    data = parse_input(input_file)
    result_second = second_part(data)
    print("Result of the second part is: {}".format(result_second))

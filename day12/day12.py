import numpy as np
import string
import sys


def parse_input(input_file):
    # convert chars to height values, 'a' has height 1, 'z' has height 27, etc.
    height_dict = {k: v for k, v in zip(string.ascii_letters, range(1, 27))}

    height_dict['S'] = height_dict['a']
    height_dict['E'] = height_dict['z']

    height_map_values = []
    start, end = None, None
    for i, line in enumerate(input_file):
        line = line.strip()
        if 'S' in line:
            start = (i, line.index('S'))
        if 'E' in line:
            end = (i, line.index('E'))

        current_row = list(height_dict[c]
                           for c in line if c in height_dict.keys())
        height_map_values.append(current_row)
    return (np.array(height_map_values, dtype=int), start, end)


def is_reachable_from(a, b, height_map):
    height_a = height_map[a]
    height_b = height_map[b]
    return height_a == height_b or height_b == height_a + 1 or height_b < height_a

# simple breadth-first computation of the distance matrix for all points(!) starting from @arg point.
def compute_distance_map_for_point(point, height_map):
    visited_map = np.full(height_map.shape, 0, int)
    distance_map = np.full(height_map.shape, sys.maxsize, dtype=np.uint64)
    distance_map[point] = 0

    nodes_queue = []
    nodes_queue.append(point)
    while len(nodes_queue) > 0:
        current_node = nodes_queue.pop(0)
        if visited_map[current_node] == 1:  # if already visited just return
            continue
        visited_map[current_node] = 1  # mark as visited
        x = current_node[0]
        y = current_node[1]

        neighbours = []
        if x > 0:
            neighbours.append((x - 1, y))
        if x < height_map.shape[0] - 1:
            neighbours.append((x + 1, y))
        if y > 0:
            neighbours.append((x, y - 1))
        if y < height_map.shape[1] - 1:
            neighbours.append((x, y + 1))
        reachable_neighbours = list(
            filter(lambda n: is_reachable_from(n, current_node, height_map), neighbours))
        for n in reachable_neighbours:
            distance_map[n] = min(
                distance_map[n], distance_map[current_node] + 1)
            nodes_queue.append(n)
    return distance_map


def first_part(data):
    height_map, start, end = data[0], data[1], data[2]

    distance_map = compute_distance_map_for_point(end, height_map)
    return distance_map[start]


def second_part(data):
    height_map, end = data[0], data[2]

    # read of the starting points from the height_map as those values which have height 1.
    starting_points = np.argwhere(height_map == 1)
    # convert coordinates to tuples, so they can act as indices
    starting_points = [(x[0], x[1]) for x in starting_points]


    distance_map = compute_distance_map_for_point(end, height_map)

    distances_of_starting_points = [distance_map[start]
                                    for start in starting_points]
    return min(distances_of_starting_points)


input_file_name = "2022_python/day12/day12.txt"

with open(input_file_name) as input_file:
    data = parse_input(input_file)
    result_first = first_part(data)
    print("Result of the first part is: {}".format(result_first))

with open(input_file_name) as input_file:
    data = parse_input(input_file)
    result_second = second_part(data)
    print("Result of the second part is: {}".format(result_second))

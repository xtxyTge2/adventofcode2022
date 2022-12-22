def parse_input(input_file):
    return [*map(int, input_file.read().split("\n"))]


"""
    To handle duplicate numbers in the input data, we implement a wrapper class, called Node,
    which stores a value and an id.
"""
class Node():
    def __init__(self, value, id):
        self.value = value
        self.id = id


def mix(data, key=1, rounds=1):
    nodes_array = [Node(value=key * v, id=j) for j, v in enumerate(data)]
    # build a dictionary, so we get the node object from a given id.
    # The usage of the node class is necessary because of duplicate values in the input data.
    nodes_dict = {node.id: node for node in nodes_array}
    n = len(nodes_array)
    for _ in range(rounds):
        for id in nodes_dict.keys():
            current_node = nodes_dict[id]  # get the node object given the id.
            idx = nodes_array.index(current_node)  # find the index

            current_node = nodes_array.pop(idx)
            # note! be very careful here, its % n - 1 and not % n!
             # This cost me 5 hours and almost made me give up ......
            new_idx = (idx + current_node.value) % (n - 1)
           
            nodes_array.insert(new_idx, current_node)
    return nodes_array


def find_zero_node(nodes_array):
    for i, node in enumerate(nodes_array):
        if node.value == 0:
            return i
    else:
        return -1


def calculate_grove_coordinates(nodes_array):
    zero_idx = find_zero_node(nodes_array)
    coordinate_indices = [(zero_idx + i * 1000) %
                          len(nodes_array) for i in range(1, 4)]
    coordinate_values = [nodes_array[idx].value for idx in coordinate_indices]
    return sum(coordinate_values)


def first_part(data):
    nodes_array = mix(data)
    return calculate_grove_coordinates(nodes_array)


def second_part(data):
    nodes_array = mix(data, key=811589153, rounds=10)
    return calculate_grove_coordinates(nodes_array)


input_file_name = "2022_python/day20/day20.txt"

"""
    Test: Result of the first part is: 3
    Real: Result of the first part is: 9945

    Test: Result of the second part is: 1623178306
    Real: Result of the second part is: 3338877775442
"""
with open(input_file_name) as input_file:
    data = parse_input(input_file)
    result_first = first_part(data)
    print("Result of the first part is: {}".format(result_first))

with open(input_file_name) as input_file:
    data = parse_input(input_file)
    result_second = second_part(data)
    print("Result of the second part is: {}".format(result_second))

import ast
import functools

def compare(a, b):
    if isinstance(a, int) and isinstance(b, int):
        if a == b:
            return 0
        if a < b:
            return 1
        if a > b:
            return -1
    if isinstance(a, int) and isinstance(b, list):
        return compare([a], b)
    if isinstance(a, list) and isinstance(b, int):
        return compare(a, [b])
    if isinstance(a, list) and isinstance(b, list):
        if len(a) == 0:
            if len(b) == 0:
                return 0
            if len(b) > 0:
                return 1
        if len(a) > 0:
            if len(b) == 0:
                return -1
            if len(b) > 0:
                # zip only zips elements up to the smaller one of a and b!
                for x, y in zip(a, b):
                    if compare(x, y) != 0:
                        return compare(x, y)
                if len(a) == len(b):
                    return 0
                elif len(a) < len(b):
                    return 1
                else:
                    return -1


def is_right_order(a, b):
    return compare(a, b) >= 0


def parse_input(input_file):
    data = []

    split_input = input_file.read().split("\n\n")

    for line in split_input:
        line_split = line.split("\n")
        # this is safe :)
        left = ast.literal_eval(line_split[0])
        right = ast.literal_eval(line_split[1])

        data.append((left, right))

    return data


def first_part(data):
    indices = []
    for i, v in enumerate(data):
        if is_right_order(v[0], v[1]):
            indices.append(i + 1)
    return sum(indices)


def second_part(data):
    # flatten data array consisting of tuples of lists, 
    # ie turn [(a, b), (x, y), (u, v), ...] into [a, b, x, y, u, v, ...]
    data_flatten = [item for item_tuple in data for item in item_tuple]

    start_sentinel = [[2]]
    end_sentinel = [[6]]
    data_flatten.append(start_sentinel)
    data_flatten.append(end_sentinel)

    data_sorted = sorted(data_flatten, key=functools.cmp_to_key(compare), reverse=True)

    start_index = data_sorted.index(start_sentinel) + 1
    end_index = data_sorted.index(end_sentinel) + 1

    return start_index * end_index


input_file_name = "2022_python/day13/day13.txt"

with open(input_file_name) as input_file:
    data = parse_input(input_file)
    result_first = first_part(data)
    "Result of the first part is: 6478"
    print("Result of the first part is: {}".format(result_first))

with open(input_file_name) as input_file:
    data = parse_input(input_file)
    result_second = second_part(data)
    "Result of the second part is: 21922"
    print("Result of the second part is: {}".format(result_second))

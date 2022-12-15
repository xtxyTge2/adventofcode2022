import re
import numpy as np
import copy


def parse_input(input_file):
    pattern = re.compile(r'-?\d+')
    sensor_beacon_pairs = []

    for line in input_file:
        match = pattern.findall(line)
        match = list(map(int, match))
        if len(match) != 4:
            print("Error parsing file. Expected 4 numbers on this line: {}".format(line))
            return
        else:
            sensor = (match[0], match[1])
            beacon = (match[2], match[3])

            sensor_beacon_pairs.append((sensor, beacon))

    balls_data = []
    for (s, b) in sensor_beacon_pairs:
        distance = manhatten_distance(s, b)
        balls_data.append((s, distance))
    return balls_data


def merge_interval_list(interval_list):
    interval_list_copy = copy.deepcopy(interval_list)
    merged = []
    while len(interval_list_copy) > 0:
        current = interval_list_copy.pop(0)
        if merged == []:
            merged.append(current)
        else:
            has_merged = False
            for m in merged:
                if m.has_overlap(current):
                    m.merge_if_overlapping(current)
                    has_merged = True
                    break
            if not has_merged:
                merged.append(current)
    return merged


class Interval():
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def cardinality(self):
        if self.is_empty():
            return 0
        else:
            return self.right - self.left

    def __copy__(self):
        return Interval(copy(self.left), copy(self.right))

    def intersect(self, other):
        if self.has_overlap(other):
            intersection_left = max(self.left, other.left)
            intersection_right = min(self.right, other.right)
            self.left = intersection_left
            self.right = intersection_right

    def has_overlap(self, other):
        if self.is_empty() or other.is_empty():
            return False
        else:
            return self.left <= other.right and other.left <= self.right

    def is_empty(self):
        if self.left is None or self.right is None:
            return True
        else:
            return self.left > self.right

    def merge_if_overlapping(self, other):
        if self.has_overlap(other):
            intersection_left = min(self.left, other.left)
            intersection_right = max(self.right, other.right)

            self.left = intersection_left
            self.right = intersection_right

    def __repr__(self):
        repr_string = ""
        return "[{}, {}]".format(self.left, self.right)


def get_intersection_of_ball_and_horizontal_line(ball_middle_point, radius, line_y):
    if radius <= 0:
        return
    ball_x = ball_middle_point[0]
    ball_y = ball_middle_point[1]

    absolute_y_difference = abs(ball_y - line_y)
    # if they intersect, get the intersection, represented by an interval of the x-coordinates of the intersection.
    if absolute_y_difference <= radius:
        left_x = ball_x - (radius - absolute_y_difference)
        right_x = ball_x + (radius - absolute_y_difference)
        return Interval(left_x, right_x)


def manhatten_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def compute_intersection_intervals(balls, line_y, cutoff_interval=None):
    intersection_intervals = []
    for (middle_point, radius) in balls:
        intersection = get_intersection_of_ball_and_horizontal_line(
            middle_point, radius, line_y)
        if intersection is not None:
            intersection_intervals.append(intersection)
    if cutoff_interval is not None:
        for m in intersection_intervals:
            m.intersect(cutoff_interval)

    merged = merge_interval_list(intersection_intervals)
    merged = merge_interval_list(merged)
    return merged


def cardinality(interval_list):
    merged = merge_interval_list(interval_list)
    cardinalities = map(lambda x: x.cardinality(), merged)
    return sum(cardinalities)


def first_part(balls_data):
    # line_y = 10 for test input, line_y = 2000000 for real input file.
    intersection_intervals = compute_intersection_intervals(
        balls_data, line_y=2000000)
    return cardinality(intersection_intervals)


def second_part(balls_data):
    cutoff_interval = Interval(0, 4000000)

    for line_y in range(cutoff_interval.left, cutoff_interval.right):
        intersection_intervals = compute_intersection_intervals(balls_data, line_y, cutoff_interval=cutoff_interval)
        intersection_intervals = merge_interval_list(intersection_intervals)
        if line_y % 10000 == 0:
            print("y: {}".format(line_y, intersection_intervals))
        if len(intersection_intervals) > 1:
            # coordinates for input file: "2022_python/day15/day15.txt"
            # x = 3204400
            # y = 3219131
            intersection_intervals = sorted(intersection_intervals, key=lambda x: x.left)
            x = intersection_intervals[0].right + 1
            y = line_y
            return x * 4000000 + y


input_file_name = "2022_python/day15/day15.txt"

"""
    Input file: "2022_python/day15/day15_test.txt"
    Result of the first part is: 26
    Result of the second part is: 56000011

    Input file: "2022_python/day15/day15.txt"
    Result of the first part is: 5181556
    Result of the second part is: 12817603219131
"""

with open(input_file_name) as input_file:
    data = parse_input(input_file)
    result_first = first_part(data)
    print("Result of the first part is: {}".format(result_first))

with open(input_file_name) as input_file:
    data = parse_input(input_file)
    result_second = second_part(data)
    print("Result of the second part is: {}".format(result_second))

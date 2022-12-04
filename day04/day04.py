"""
Interval class. Does allow __non-valid__ interval objects where its right boundary
is smaller than its left boundary.
"""
class interval:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def is_contained_in(self, other):
        return self.left <= other.left and self.right >= other.right

    def __repr__(self):
        return "Interval object: ({}, {})".format(self.left, self.right)

    def has_overlap_with(self, other):
        intersection = self.get_intersection(other)
        return not intersection.is_empty()    

    def get_intersection(self, other):
        left = max(self.left, other.left)
        right = min(self.right, other.right)
        return interval(left, right)

    def is_empty(self):
        return self.left > self.right


"""
Parse the input line by line. Split each line into its two parts and parse 
the left and right hand side into interval objects. For each line put 
the left and right side interval object into a tuple and add this tuple into
a list. Returns this list.
"""
def parse_input(input_file):
    data = []
    for line in input_file:
        split = line.rstrip().split(",")

        a = split[0].split("-")
        b = split[1].split("-")

        a_left = int(a[0])
        a_right = int(a[1])

        b_left = int(b[0])
        b_right = int(b[1])

        x = interval(a_left, a_right)
        y = interval(b_left, b_right)
        
        data.append((x, y))
    return data

"""
Helper wrapper function. Unwraps a tuple object containing two interval objects 
and checks if one is contained in the other.
"""
def one_contains_the_other(interval_tuple):
    x = interval_tuple[0]
    y = interval_tuple[1]
    return x.is_contained_in(y) or y.is_contained_in(x)

"""
Helper wrapper function. Unwraps a tuple object containing two interval objects
and checks if these two intervals have non-empty overlap.
"""
def has_overlap(interval_tuple):
    x = interval_tuple[0]
    y = interval_tuple[1]
    return x.has_overlap_with(y)

def first_part(data):
    return len(list(filter(lambda t: one_contains_the_other(t), data)))

def second_part(input_file):
    return len(list(filter(lambda t: has_overlap(t), data))) 

input_file_name = "day05.txt"

with open(input_file_name) as input_file:
    data = parse_input(input_file)
    result_first = first_part(data)
    print("Result of the first part is: {}".format(result_first))

with open(input_file_name) as input_file:
    data = parse_input(input_file)
    result_second = second_part(data)
    print("Result of the second part is: {}".format(result_second))

import string

def has_duplicate_characters(values):
    count_dict = dict.fromkeys(string.ascii_lowercase, 0)
    for v in values:
        count_dict[v] += 1
    return len(list(filter(lambda count: count >= 2, count_dict.values())))

def find_signal_marker(string, signal_marker_length):
    string = string.rstrip()
    if not string or len(string) < signal_marker_length: return

    values = list(string[:signal_marker_length])
    for i in range(signal_marker_length, len(string)):
        pop = values.pop(0)
        values.append(string[i])
        if not has_duplicate_characters(values):
            return i + 1
    return -1


def parse_input(input_file):
    return input_file 

def find_signal_markers_in_data(data, signal_marker_length):
    signal_markers = list(map(lambda x: find_signal_marker(x, signal_marker_length)
        , data.readlines()))
    if len(signal_markers) == 1:
        return signal_markers[0]    
    else: 
        return signal_markers
    return None

def first_part(data):
    return find_signal_markers_in_data(data, 4)

def second_part(data):
    return find_signal_markers_in_data(data, 14)

input_file_name = "day06.txt"

with open(input_file_name) as input_file:
    data = parse_input(input_file)
    result_first = first_part(data)
    print("Result of the first part is: {}".format(result_first))

with open(input_file_name) as input_file:
    data = parse_input(input_file)
    result_second = second_part(data)
    print("Result of the second part is: {}".format(result_second))

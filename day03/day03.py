import string

def first_part(input_file):
    priorities = []
    for line in input_file:
        line = line.rstrip()

        half = int(len(line)/2)
        first = line[:half]
        second = line[half:]
        
        first_count_dict = dict.fromkeys(string.ascii_letters, 0)
        for c in first:
            first_count_dict[c] += 1
        second_count_dict = dict.fromkeys(string.ascii_letters, 0)
        for c in second:
            second_count_dict[c] += 1

        for c in string.ascii_letters:
            if first_count_dict[c] != 0 and second_count_dict[c] != 0:
                key = string.ascii_letters.index(c)
                priorities.append(key + 1) # add 1, since its 0 index based 
    return sum(priorities)

def second_part(input_file):
    priorities = []
    lines = input_file.readlines()
    line_num = len(lines)
    for i in range(0, line_num, 3):
        line1 = lines[i].rstrip()
        line2 = lines[i + 1].rstrip()
        line3 = lines[i + 2].rstrip()
        
        first_count_dict = dict.fromkeys(string.ascii_letters, 0)
        for c in line1:
            first_count_dict[c] += 1

        second_count_dict = dict.fromkeys(string.ascii_letters, 0)
        for c in line2:
            second_count_dict[c] += 1

        third_count_dict = dict.fromkeys(string.ascii_letters, 0)
        for c in line3:
            third_count_dict[c] += 1

        for c in string.ascii_letters:
            if first_count_dict[c] != 0 and second_count_dict[c] != 0 and third_count_dict[c] != 0:
                key = string.ascii_letters.index(c)
                priorities.append(key + 1) # add 1, since its 0 index based 
    return sum(priorities)

if __name__ == '__main__':
    input_file_name = "day03.txt"
    with open(input_file_name) as input_file:
        result_first = first_part(input_file)
        print("Result of the first part is: {}.".format(result_first))

    with open(input_file_name) as input_file:
        result_second = second_part(input_file)
        print("Result of the second part is: {}".format(result_second))

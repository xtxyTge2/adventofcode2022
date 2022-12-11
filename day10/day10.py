import numpy as np

def parse_input(input_file):
    register = 1
    cycle = 0

    data = []
    for line in input_file:
        line_split = line.rstrip().split(" ")
        if line_split[0] == "noop":
            cycle += 1
            data.append((cycle, register))
        if line_split[0] == "addx":
            cycle += 1
            data.append((cycle, register))
            cycle += 1
            data.append((cycle, register))
    cycle += 1
    data.append((cycle, register))
    return data

def signal_strength(register_data):
    f = [(x, y, x*y) for x, y in register_data if x in [20, 60, 100, 140, 180, 220]]
    return sum([z for (x, y, z) in f])

def first_part(data):
    return signal_strength(data)

def second_part(input_file):
    screen = np.full((6, 40), "", np.unicode_)

    lines = input_file.readlines()
    executing_instruction = False
    value = 0
    line = None
    sprite_pos = [0, 1, 2]
    sprite_array = np.full((40), ".", np.unicode_)
    for v in sprite_pos:
        sprite_array[v] = "#"
    sprite_str = "".join([v for v in sprite_array])
    repr_string  = "Sprite position: {}\n".format(sprite_str) 
    print(repr_string)   
    for i in range(240):
        cycle = i + 1
        repr_string = ""
        coord_x = i % 40 
        coord_y = i // 40
        if not executing_instruction:
            if len(lines) > 0:
                line = lines.pop(0)
            else:
                line = None
            if line is not None:
                line_split = line.rstrip().split(" ")
                if line_split[0] == "noop":
                    repr_string += "Start cycle {}: begin executing noop\n".format(cycle)
                    repr_string += "During cycle {}: CRT draws pixel in position {}\n".format(cycle, coord_x)
                    repr_string += "Current CRT row: " + "".join(screen[coord_y]) + "\b"
                    if coord_x in sprite_pos:
                        screen[coord_y, coord_x] = "#"
                    else:
                        screen[coord_y, coord_x] = "."
                    repr_string += "End of cycle {}: finish executing noop\n".format(cycle)
                elif line_split[0] == "addx":
                    executing_instruction = True
                    value = int(line_split[1])
                    repr_string += "Start cycle {}: begin executing addx {}\n".format(cycle, value)
                    repr_string += "During cycle {}: CRT draws pixel in position {}\n".format(cycle, coord_x)
                    if coord_x in sprite_pos:
                        screen[coord_y, coord_x] = "#"
                    else:
                        screen[coord_y, coord_x] = "."

                    repr_string += "Current CRT row: " + "".join(screen[coord_y]) + "\n"
        else:
                # only case is that the executing instruction is an addx instruction
                executing_instruction = False
                repr_string += "During cycle {}: CRT draws pixel in position {}\n".format(cycle, coord_x)
                if coord_x in sprite_pos:
                    screen[coord_y, coord_x] = "#"
                else:
                    screen[coord_y, coord_x] = "."
                repr_string += "Current CRT row: " + "".join(screen[coord_y]) + "\n"

                sprite_pos += np.array([value, value, value])
                repr_string += "End of cycle {}: finish executing addx {} (Register X is now {})\n".format(cycle, value, 1 + sprite_pos[0])
                
                value = 0 # reset value

                sprite_array = np.full((40), ".", np.unicode_)
                for v in sprite_pos:
                    if v in range(0, 40):
                        sprite_array[v] = "#"
                sprite_str = "".join([v for v in sprite_array])
                repr_string  += "Sprite position: {}\n".format(sprite_str)
        print(repr_string)
        #pretty_print(screen)
    print("Final CRT screen:")
    pretty_print(screen)
    return None 

def pretty_print(screen):
    repr_string = ""
    for row in screen:
        for v in row:
            repr_string += str(v)
        repr_string += "\n"
    print(repr_string)

input_file_name = "2022_python/day10/day10.txt"

with open(input_file_name) as input_file:
    instructions = parse_input(input_file)
    result_first = first_part(instructions)
    print("Result of the first part is: {}".format(result_first))

with open(input_file_name) as input_file:
    result_second = second_part(input_file)
    print("Result of the second part is: {}".format(result_second))

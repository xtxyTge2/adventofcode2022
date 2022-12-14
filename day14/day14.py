import numpy as np

def parse_input(input_file, add_bottom_part=False): 
    # yeah this is unreadable, but its fun... 
    data = list(map(lambda l: list(map(lambda y: list(map(lambda z: int(z), y.strip(
    ).split(","))), l)), map(lambda x: x.split("->"), input_file.read().split("\n"))))

    coordinate_split = list(zip(*[x for y in data for x in y]))

    start_coord = [500, 0]
    x_coords = coordinate_split[0]
    # append x-coordinate of sand corn starting coordinate
    x_coords = x_coords + (500, )
    y_coords = coordinate_split[1]
    # append y-coordinate of sand corn starting coordinate
    y_coords = y_coords + (0, )

    x_min, x_max = min(x_coords), max(x_coords)
    y_min, y_max = min(y_coords), max(y_coords)

    # this is used in the second part
    if add_bottom_part:
        y_max += 2
        x_min -= y_max + 1
        x_max += y_max + 1

        data.append([[x_min, y_max], [x_max, y_max]])

    origin = (x_min, y_min)
    top_left_corner = origin
    bottom_right_corner = (x_max + 1, y_max + 1)

    shape = (bottom_right_corner[0] - top_left_corner[0],
             bottom_right_corner[1] - top_left_corner[1])
    normalized_start_coordinate = (start_coord[0] - origin[0],
                                   start_coord[1] - origin[1])

    grid = np.full(shape=shape, fill_value=" ", dtype=np.unicode_)
    

    normalized_coords = [[(coord[0]-origin[0], coord[1]-origin[1])
                          for coord in l] for l in data]
    drawing_pairs_data = [[(l[i - 1], l[i]) for i in range(len(l)) if i > 0]
                          for l in normalized_coords]   

    for l in drawing_pairs_data:
        for coord_pair in l:
            draw_line(grid, coord_pair[0], coord_pair[1])

    return (grid, normalized_start_coordinate)

def is_inside(a, grid):
    return a[0] >= 0 and a[0] < grid.shape[0] and a[1] >= 0 and a[1] < grid.shape[1]

def get_next_coord(grid, sand_coord):
    x, y = sand_coord[0], sand_coord[1]

    bottom = (x, y + 1)
    bottom_left = (x - 1, y + 1)
    bottom_right = (x + 1, y + 1)

    next_coords = []
    next_coords.append(bottom)
    next_coords.append(bottom_left)
    next_coords.append(bottom_right)

    for next in next_coords:
        if not is_inside(next, grid):
            return (-1, -1)  # sand corn falls to infinity
        if grid[next] == " ":
            return next
    return sand_coord

def let_sandcorn_fall(grid, start_coord):
    if grid[start_coord] == "o":
        return (-1, -1)
    sand_coord = start_coord  # hardcoded starting coordinate defined in exercise

    next_coord = get_next_coord(grid, sand_coord)
    while (next_coord != sand_coord):
        sand_coord = next_coord
        next_coord = get_next_coord(grid, sand_coord)
        if next_coord == (-1, -1):
            return (-1, -1)  # sand corn falls to infinity
    return sand_coord

def draw_line(grid, a, b):
    a_x, a_y = a[0], a[1]
    b_x, b_y = b[0], b[1]

    if a_x == b_x or a_y == b_y:
        # only draw vertical or horizontal lines
        start_x, end_x = min(a_x, b_x), max(a_x, b_x) + 1
        start_y, end_y = min(a_y, b_y), max(a_y, b_y) + 1
        grid[start_x:end_x, start_y:end_y] = "#"

def pretty_print(grid):
    grid = grid.T  # due to numpy and our coordinate system conventions we always print the transpose

    repr_string = "\n".join(
        ["".join([grid[i, j] for j in range(grid.shape[1])]) for i in range(grid.shape[0])])
    print(repr_string)

def simulate_falling_sand(grid, start_coord):
        max_iterations = 1000000
        for i in range(1, max_iterations):
            next_sand_coord = let_sandcorn_fall(grid, start_coord=start_coord)
            if next_sand_coord == (-1, -1):
                return (grid, i)
            else:
                grid[next_sand_coord] = "o"
        return (grid, max_iterations)

def first_part(input_file, print_state=False):
    data = parse_input(input_file, add_bottom_part=False)
    grid, start_coord = data[0], data[1]

    (grid, iterations) = simulate_falling_sand(grid, start_coord)
    if print_state:
        print("Final grid after {} iterations:".format(iterations))
        pretty_print(grid)
    return iterations

def second_part(input_file, print_state=False):
    data = parse_input(input_file, add_bottom_part=True)
    grid, start_coord = data[0], data[1]

    (grid, iterations) = simulate_falling_sand(grid, start_coord)
    if print_state:
        print("Final grid after {} iterations:".format(iterations))
        pretty_print(grid)
    return iterations

input_file_name = "2022_python/day14/day14.txt"

"""
Result of the first part is: 675
Result of the second part is: 24959
"""

with open(input_file_name) as input_file:
    result_first = first_part(input_file)
    print("Result of the first part is: {}".format(result_first))

with open(input_file_name) as input_file:
    result_second = second_part(input_file)
    print("Result of the second part is: {}".format(result_second))
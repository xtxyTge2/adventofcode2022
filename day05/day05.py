class CrateMoveOrder():
    def __init__(self, num_objects, src_crate, dest_crate):
        self.num_objects = num_objects
        self.src_crate = src_crate
        self.dest_crate = dest_crate

    def __repr__(self):
        return "CrateMoveOrder: Number of objects to move: {}, Source: {}, Destination: {}"\
                .format(self.num_objects, self.src_crate, self.dest_crate)
    
class CrateStockpile():
    def __init__(self, num_crates, crates):
        self.num_crates = num_crates
        self.crates = crates

    def execute_move_order(self, move_order, reverse_crates_when_moving: False):
        num_objects = move_order.num_objects
        src_id = move_order.src_crate
        dest_id = move_order.dest_crate
        if num_objects <= 0 \
                or src_id < 0 or src_id > self.num_crates \
                or dest_id < 0 or dest_id > self.num_crates: 
                    return 

        src = self.crates[src_id]
        dest = self.crates[dest_id]
        objects_to_move = src[-num_objects:]
        
        self.crates[src_id] = src[:-len(objects_to_move) or None]
        if reverse_crates_when_moving: 
            self.crates[dest_id] = dest + list(reversed(objects_to_move))
        else:
            self.crates[dest_id] = dest + list(objects_to_move)



    def __repr__(self):
        string_repr = []
        string_repr.append("CrateStockpile object: number of crates: {}"\
                .format(self.num_crates))
        for i, crate in enumerate(self.crates):
            string_repr.append("{}: ".format(i) + str(crate))
        return "\n".join(string_repr)


def parse_input(input_file):
    crate_position_lines = []
    move_order_lines = []
    

    crate_definition_line = ""
    parsed_crate_definition_line = False
    parsing_crate_positions = True
    for line in input_file:
        if not parsed_crate_definition_line and "1" in line:
            crate_definition_line = line
            parsed_crate_definition_line = True
            parsing_crate_positions = False
            continue
        if parsing_crate_positions:
            crate_position_lines.append(line)
        
        if "move" in line:
            move_order_lines.append(line)


    # parse crate data
    crate_ids = crate_definition_line
    crate_position_index = []
    for i, c in enumerate(crate_ids):
        if c.isalnum():
            crate_position_index.append((i, int(c)))

    crates_raw = []
    num_of_crates = len(crate_position_index)
    for (i, v) in crate_position_index:
        current_crate = []
        for line in reversed(crate_position_lines):
            if line[i].strip():
                current_crate.append(line[i])
        crates_raw.append(current_crate)
    crate_stockpile = CrateStockpile(num_of_crates, crates_raw) 
    
    # parse move orders
    move_orders = []
    for line in move_order_lines:
        line_split = line.rstrip().split(" ")
        num_objects = int(line_split[1])
        src_crate = int(line_split[3]) - 1 # crates are 0 index based internally
        dest_crate = int(line_split[5]) - 1 # crates are 0 index based interally

        move_orders.append(CrateMoveOrder(num_objects, src_crate, dest_crate))
    
    return (crate_stockpile, move_orders)

def execute_move_orders(data, show_execution: False, reverse_move_order_when_moving):
    crate_stockpile = data[0]
    move_orders = data[1]
    if show_execution:
        print(crate_stockpile)
    for move_order in move_orders:
        if show_execution:
            print(move_order)
            print(crate_stockpile)
            print("".join(["#" for i in range(80)]))
        crate_stockpile.execute_move_order(move_order, reverse_move_order_when_moving)
    
    if show_execution:
        print(crate_stockpile)
    result = ""
    for crate in crate_stockpile.crates:
        result += str(crate[-1])
    return result

def first_part(data, show_execution: False):
    return execute_move_orders(data, show_execution, reverse_move_order_when_moving=True)

def second_part(data, show_execution: False):
    return execute_move_orders(data, show_execution, reverse_move_order_when_moving=False)

input_file_name = "day05.txt"

with open(input_file_name) as input_file:
    data = parse_input(input_file)
    result_first = first_part(data, show_execution=False)
    print("Result of the first part is: {}".format(result_first))

with open(input_file_name) as input_file:
    data = parse_input(input_file)
    result_second = second_part(data, show_execution=False)
    print("Result of the second part is: {}".format(result_second))

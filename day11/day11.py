import math

class Monkey():
    def __init__(self, id, items, operation_str, test_str, test_value, test_true, test_false):
        self.id = id
        self.items = items
        self.operation_str = operation_str
        self.test_str = test_str
        self.test_value = test_value
        self.test_true = test_true
        self.test_false = test_false
        self.num_items_inspected = 0

    def test(self, x):
        return x % self.test_value == 0 

    def __repr__(self):
        repr_string = "Monkey {}:\n".format(self.id)
        repr_string += "    Starting items: " + ", ".join([str(v) for v in self.items])
        repr_string += "\n"
        repr_string += "    Operation: {}\n".format(self.operation_str)
        repr_string += "    Test: {}\n".format(self.test_str)
        repr_string += "        If true: throw to monkey {}\n".format(self.test_true)
        repr_string += "        If false: throw to monkey {}\n".format(self.test_false)
        return repr_string

    def operation(self, x):
        line_split = self.operation_str.strip().split(" ")
        arg1 = line_split[2]
        op = line_split[3]
        arg2 = line_split[4]

        if op == "+":
            if arg1 == "old":
                if arg2 == "old":
                    return (x + x)
                else:
                    return (x + int(arg2)) 
            else:
                if arg2 == "old":
                    return (int(arg1) + x)
                else:
                    return (int(arg1) + int(arg2)) 
        if op == "-":
            if arg1 == "old":
                if arg2 == "old":
                    return x - x
                else:
                    return (x - int(arg2)) 
            else:
                if arg2 == "old":
                    return (int(arg1) - x) 
                else:
                    return (int(arg1) - int(arg2)) 
        if op == "*":
            if arg1 == "old":
                if arg2 == "old":
                    return x * x
                else:
                    return (x * int(arg2)) 
            else:
                if arg2 == "old":
                    return (int(arg1) * x) 
                else:
                    return (int(arg1) * int(arg2))
        if op == "/":
            if arg1 == "old":
                if arg2 == "old":
                    return (x / x)
                else:
                    return (x / int(arg2))
            else:
                if arg2 == "old":
                    return (int(arg1) / x)
                else:
                    return (int(arg1) / int(arg2))

    def inspect_items_first_part(self, monkeys):
        repr_string = "Monkey: {}\n".format(self.id)
        if len(self.items) == 0:
            repr_string = "     Monkey has no items to inspect.\n"
        else:
            while len(self.items) > 0:
                self.num_items_inspected += 1
                it = self.items.pop(0)
                repr_string += "    Monkey inspects an item with a worry level of {}.\n".format(it)
                
                it = self.operation(it)
                repr_string += "        New worry level is {}, operation: {}\n".format(it, self.operation_str)
                it = it // 3
                repr_string += "        Monkey gets bored with item. Worry level is modulo to {}.\n".format(it)

                if self.test(it):
                    repr_string += "        Current worry level is divisible by {}.\n".format(self.test_value)
                    repr_string += "        Item with worry level {} is thrown to monkey {}.\n".format(it, self.test_true)
                    other_monkey = monkeys[self.test_true]
                else:
                    repr_string += "        Current worry level is not divisible by {}.\n".format(self.test_value)
                    repr_string += "        Item with worry level {} is thrown to monkey {}.\n".format(it, self.test_false)
                    other_monkey = monkeys[self.test_false]
                other_monkey.items.append(it)

        #print(repr_string)

    def inspect_items_second_part(self, monkeys, reduction):
            repr_string = "Monkey: {}\n".format(self.id)
            if len(self.items) == 0:
                repr_string = "     Monkey has no items to inspect.\n"
            else:
                while len(self.items) > 0:
                    self.num_items_inspected += 1
                    it = self.items.pop(0)
                    repr_string += "    Monkey inspects an item with a worry level of {}.\n".format(it)
                    
                    it = self.operation(it) 
                    repr_string += "        New worry level is {}, operation: {}\n".format(it, self.operation_str)
                    #it = it // 3
                    it = it % reduction
                    repr_string += "        Monkey gets bored with item. Worry level is modulo to {}.\n".format(it)

                    if self.test(it):
                        repr_string += "        Current worry level is divisible by {}.\n".format(self.test_value)
                        repr_string += "        Item with worry level {} is thrown to monkey {}.\n".format(it, self.test_true)
                        other_monkey = monkeys[self.test_true]
                    else:
                        repr_string += "        Current worry level is not divisible by {}.\n".format(self.test_value)
                        repr_string += "        Item with worry level {} is thrown to monkey {}.\n".format(it, self.test_false)
                        other_monkey = monkeys[self.test_false]
                    other_monkey.items.append(it)

            #print(repr_string)


def run_round_first_part(id, monkeys):
    for m in monkeys:
        m.inspect_items_first_part(monkeys)
    repr_string = "After round {}, the monkeys are holding items with"\
        "these worry levels:\n".format(id)
    for m in monkeys:
        repr_string += "Monkey {}: ".format(m.id)
        repr_string += ", ".join([str(v) for v in m.items]) + "\n"
    print(repr_string)
   

def run_round_second_part(id, monkeys, lcm):
    for m in monkeys:
        m.inspect_items_second_part(monkeys, lcm)
    repr_string = "After round {}, the monkeys are holding items with"\
        "these worry levels:\n".format(id)
    for m in monkeys:
        repr_string += "Div: {}, Monkey {}: ".format(m.test_value, m.id)
        repr_string += ", ".join([str(v) for v in m.items]) + "\n"
    #print(repr_string)


def parse_input(input_file):
    monkeys = []
    for line in input_file:
        line = line.strip()
        line_split = line.split(" ")
        if len(line.strip()) == 0:
            continue
        if line_split[0] == "Monkey":
            id = int(line_split[1].strip(":"))
            items = []
            operation_str = ""
            test_str = ""
            test_value = None
            test_true = -1
            test_false = -1
        elif line_split[0] == "Starting":
            for v in "".join(line_split[2:]).split(","):
                items.append(int(v))
        elif line_split[0] == "Operation:":
            operation_str = " ".join(line_split[1:])
        elif line_split[0] == "Test:":
            test_str = line.strip()
            test_value = int(line_split[3])
        elif line_split[0] == "If" and line_split[1] == "true:":
            test_true = int(line_split[5])
        elif line_split[0] == "If" and line_split[1] == "false:":
            test_false = int(line_split[5])
            monkeys.append(Monkey(id, items, operation_str, test_str, test_value, test_true, test_false))
            # finished parsing
    return monkeys
            
def first_part(monkeys):
    for r in range(1, 21):
        #print(r)
        #print()
        run_round_first_part(r, monkeys)
       
        repr_string = "Round: {}.\n".format(r)
        for m in monkeys:
            repr_string += "Monkey {} inspected items {} times.\n"\
            .format(m.id, m.num_items_inspected)
        print(repr_string)
    
    repr_string = ""
    for m in monkeys:
        repr_string += "Monkey {} inspected items {} times.\n"\
            .format(m.id, m.num_items_inspected)
    print(repr_string)

    x, y = sorted([m.num_items_inspected for m in monkeys])[-2:]
    return x * y

def second_part(monkeys):
    lcm = math.lcm(*[m.test_value for m in monkeys])

    for r in range(1, 10001):
        #print(r)
        #print()
        run_round_second_part(r, monkeys, lcm)
        if r % 1000 == 0 or r == 20 or r == 1:
            repr_string = "Round: {}.\n".format(r)
            for m in monkeys:
                repr_string += "Monkey {} inspected items {} times.\n"\
                .format(m.id, m.num_items_inspected)
            print(repr_string)
        #print(r)
        #print()
    
    repr_string = ""
    for m in monkeys:
        repr_string += "Monkey {} inspected items {} times.\n"\
            .format(m.id, m.num_items_inspected)
    print(repr_string)

    x, y = sorted([m.num_items_inspected for m in monkeys])[-2:]
    return x * y

input_file_name = "2022_python/day11/day11.txt"

with open(input_file_name) as input_file:
    monkeys = parse_input(input_file)
    result_first = first_part(monkeys)
    print("Result of the first part is: {}".format(result_first))

with open(input_file_name) as input_file:
    monkeys = parse_input(input_file)
    result_second = second_part(monkeys)
    print("Result of the second part is: {}".format(result_second))

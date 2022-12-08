class Node():
    def __init__(self, name, filetype, internal_size, parent=None, children=None):
        self.name = name
        self.parent = None
        self.children = set()
        self.internal_size = internal_size
        self.filetype = filetype

    def get_size(self):
        if self.filetype == "file":
            return self.internal_size
        else:
            if not self.children is None:
                return sum(map(Node.get_size, self.children))
            else:
                return 0

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.name == other.name and \
            self.parent == other.parent and \
                self.size == other.size and \
                    self.filetype == other.filetype
        else:
            return False

    def add_children(self, node):
        if node:
            node.parent = self
            self.children.add(node)
            
    def get_list_of_children(self, nodes):
        nodes.append(self)    
        if self.children:
            for child in self.children:
                child.get_list_of_children(nodes)

    def internal_repr(self, depth=0, highlight_node=None):
        repr_string = ""
        if True or self.filetype == "dir":
            repr_string = "- {} ({}, size={})".format(self.name, self.filetype, self.get_size())
            if self == highlight_node:
                repr_string += " <--- current_node"
            repr_string += "\n"
            if self.children:
                depth += 1
                repr_string += "\n".join(map(lambda x: "".join([" " for i in range(depth)]) 
                + Node.internal_repr(x, depth, highlight_node), 
                self.children))
        return repr_string
    
    def __repr__(self):
        return self.internal_repr(depth=0)

class FileSystemCommand():
    def __init__(self, name, argument=None, filesystem=None):
        self.filesystem = filesystem
        self.name = name
        self.argument = argument
        self.output = []

    def append_output(self, output):
        self.output.append(output)
    def __repr__(self):
        if self.argument:
            result = "$ {} {}".format(self.name, self.argument)
        else: 
            result = "$ {}".format(self.name)

        if self.output:
            result += "\nOutput:\n"
            result += "\n".join(self.output)
        return result

class FileSystemCommandListFile(FileSystemCommand):
    def __execute__(self):
        for node in self.output:
            self.filesystem.add_children(self.filesystem.current_node, node)       

class FileSystemCommandChangeDirectory(FileSystemCommand):
    def __execute__(self):
        if self.argument == "..":
            self.filesystem.cd_upwards()
        else:
            self.filesystem.cd_downwards(self.argument)

class FileSystem():
    def __init__(self, root, commands=None):
        self.root = root
        self.current_node = self.root
        self.commands = commands
        if commands is not None:
            for cmd in commands:
                cmd.filesystem = self

    
    def add_children(self, parent, node):
        parent.add_children(node)

    def execute_commands(self):
        for cmd in self.commands:
            cmd.__execute__()

    def get_list_of_nodes(self):
        nodes = []
        self.root.get_list_of_children(nodes)
        return nodes

    def __repr__(self):
        return self.root.internal_repr(depth=0, highlight_node=self.current_node)
        
    def cd_downwards(self, children_name):
        if self.current_node.children is None:
            print("Error traversing filesystem. Node name: {} has "\
                    "no children named {}, line: {}."\
                    .format(self.current_node.name, children_name)) 
            return False
        found_children = False
        for child in self.current_node.children:
            if child.name == children_name:
                self.current_node = child
                found_children = True
                break
        return found_children
    def cd_upwards(self):
        if not self.current_node.parent is None:
            self.current_node = self.current_node.parent
        else:
            print("Error! Cant traverse upwards from directory {},"\
                "it has no parent directory.".format(self.current_node))
  


def parse_input(input_file):
    commands = []
    current_command = None
    for line in input_file:
        line_split = line.rstrip().split(" ")
        if line_split[0] == "$":
            parsing_command_output = False

            command_name = line_split[1]
            command_argument = None
            if len(line_split) >= 3:
                command_argument = line_split[2]
            if command_name == "cd":
                current_command = FileSystemCommandChangeDirectory(command_name, command_argument)
            if command_name == "ls":
                current_command = FileSystemCommandListFile(command_name, command_argument)
            commands.append(current_command)
            parsing_command_output = True
        elif parsing_command_output:
            line_split = line.rstrip().split(" ")
            
            filetype_arg = line_split[0]
            name = line_split[1]
            
            if filetype_arg == "dir":
                filetype = "dir"
                size = 0
            else:
                filetype = "file"
                size = int(line_split[0])
            new_node = Node(name, filetype, size)
            current_command.append_output(new_node)
    return commands

def create_filesystem_and_execute_commands(input_file):
    root = Node("/", "dir", 0)
    commands = parse_input(input_file)
    filesystem = FileSystem(root, commands=commands)
    filesystem.execute_commands()
    return filesystem

def first_part(input_file):
    filesystem = create_filesystem_and_execute_commands(input_file)
    nodes = filesystem.get_list_of_nodes() # get list of all nodes in filesystem

    max_value = 100000 
    filtered_nodes = filter(lambda x: x.filetype == "dir" and x.get_size() <= max_value, nodes)
    return sum(map(lambda x: x.get_size(), filtered_nodes))
    

def second_part(data):
    filesystem = create_filesystem_and_execute_commands(input_file)
    nodes = filesystem.get_list_of_nodes()

    available_total_diskspace = 70000000
    needed_free_space = 30000000
    current_diskspace = available_total_diskspace - filesystem.root.get_size()
    space_needed = needed_free_space - current_diskspace

    potential_directories_to_delete = filter(lambda x: x.filetype == "dir" and x.get_size() >= space_needed, nodes)
    return min(map(lambda x: x.get_size(), potential_directories_to_delete)) 

input_file_name = "day07.txt"

with open(input_file_name) as input_file:
    result_first = first_part(input_file)
    print("Result of the first part is: {}".format(result_first))

with open(input_file_name) as input_file:
    result_second = second_part(input_file)
    print("Result of the second part is: {}".format(result_second))
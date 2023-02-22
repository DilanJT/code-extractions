import tree_sitter
from collections import defaultdict


LANGUAGE = tree_sitter.Language('parser/my-languages.so','python')
parser = tree_sitter.Parser()
parser.set_language(LANGUAGE)

data_flow_graph = defaultdict(set)

def extract_dfg(code):
    
    # Parse the code using the python language parser
    tree = parser.parse(code.encode('utf-8'))

    print("tree count : ", tree.root_node.child_count)
    print("tree : ", tree.root_node.children)

    # Traverse the syntax tree and extract the data flow graph
    for node in tree.root_node.children:
        print("(inside extract_dfg) node : ", node.type)
        if node.type == 'expression_statement':
            print("node : ", node.type)
            # if the node is a variable name, add it to the data flow graph
            var_name = code[node.start_byte:node.end_byte]
            print("\nparent node : ", node)
            data_flow_graph[var_name].update(get_input_vars(node, code))

    return data_flow_graph


def get_input_vars(node, code):
    # Recursively traverse the syntax tree to find the inputs to an operation
    inputs = set()
    print("(inside get_input_vars) node type : ", node.type)
    if node.type == 'call':
        # If the node is a function call, add the function name to the inputs
        for child in node.children:
            if child.type == 'argument_list':
                for arg in child.children:
                    if arg.type == 'name':
                        inputs.add(code[arg.start_byte:arg.end_byte])
                    else:
                        inputs.update(get_input_vars(arg, code))

    elif node.type == 'binary_expression':
        # If the node is a binary operation, add its operands to the inputs
        for child in node.children:
            if child.type == 'name':
                inputs.add(code[child.start_byte:child.end_byte])
            else:
                inputs.update(get_input_vars(child, code))

    elif node.type == 'unary_expression':
        # If the node is an assignment, add the variable name to the inputs
        for child in node.children:
            if child.type == 'name':
                inputs.add(code[child.start_byte:child.end_byte])
            else:
                inputs.update(get_input_vars(child, code))

    print("inputs : ", inputs)
    return inputs


code = """
def add(x, y):
    return x + y

def multiply(x, y):
    return add(x, y) * y

z = add(2, 3)
w = multiply(z, 4)

def greet(name):
    print('Hello', name)
"""

data_flow_graph_full = extract_dfg(code)

# print the data flow graph

for var_name, inputs in extract_dfg(code).items():
    print(var_name, '->', inputs)

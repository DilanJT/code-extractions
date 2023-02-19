import tree_sitter
import sys

### STILL IN DEVELOPMENT ###

# Download and compile the Python language grammar
# This only needs to be done once




LANGUAGE = tree_sitter.Language('parser/my-languages.so','python')

# define a function that extract function definition and their arguments
def extract_functions_code(code):
    # parse the code using the python language parser

    parser = tree_sitter.Parser()
    parser.set_language(LANGUAGE)

    tree = parser.parse(code.encode('utf-8'))

    # list of functions and their arguments
    functions = []
    
    # Traverse the syntax tree and extract the function definitions and their arguments
    for node in tree.root_node.children:
        if node.type == 'function_definition':
            # Extract the name of the function
            name_node = node.child_by_field_name('name')
            name = code[name_node.start_byte:name_node.end_byte]

            print("name : ", name)

            # Extract the names of the arguments
            arguments = []
            for param_node in node.child_by_field_name('parameters').children:
                if param_node.type == 'name':
                    argument = code[param_node.start_byte:param_node.end_byte]
                    arguments.append(argument)

            # Add the function definition and its arguments to the list
            functions.append((name, arguments))

    return functions


code = """
def add(x, y):
    return x + y

def multiply(x, y):
    return x * y

z = add(2, 3)
w = multiply(z, 4)
"""

# Extract the function definitions and their arguments from the input code
functions = extract_functions_code(code)

# Print the function definitions and their arguments
for name, arguments in functions:
    print('Function:', name)
    print('Arguments:', ', '.join(arguments))
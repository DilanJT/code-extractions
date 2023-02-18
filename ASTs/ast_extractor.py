import ast

def extract_ast_file(filename):
    with open(filename) as f:
        parsed =  ast.parse(f.read(), filename)

    # convert the ast to a string
    return ast.dump(parsed)


def extract_ast_code(code):
    parsed = ast.parse(code)
    # convert the ast to a string
    return ast.dump(parsed)

# extract functions using asts
def extract_functions_code(code):
    parsed = ast.parse(code)
    functions = []
    for node in ast.walk(parsed):
        if isinstance(node, ast.FunctionDef):
            functions.append(node.name)
    return functions

print(extract_ast_code('print("Hello World!")'))
print('test :',extract_functions_code('def foo(): pass\ndef bar(): pass'))
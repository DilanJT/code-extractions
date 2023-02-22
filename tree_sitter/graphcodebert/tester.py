from utils import remove_comments_and_docstrings,tree_to_token_index,index_to_code_token
import tree_sitter
import sys

code = """
def add(x, y):
    return x + y

def multiply(x, y):
    return x * y

z = add(2, 3)
w = multiply(z, 4)

def greet(name):
    print('Hello', name)
"""

java_code = """
public class Main {
    public static void main(String[] args) {
        System.out.println("Hello, world!");
    }
}
"""

LANGUAGE = tree_sitter.Language('parser/java.so','java')
parser = tree_sitter.Parser()
parser.set_language(LANGUAGE)

singleTree = parser.parse(java_code.encode('utf-8'))
root_node = singleTree.root_node

print("tree to token index : ", tree_to_token_index(root_node))
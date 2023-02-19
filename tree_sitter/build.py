
import tree_sitter

# Download and compile the Python language grammar
# This only needs to be done once

'git clone https://github.com/tree-sitter/tree-sitter-python'

def buildTree():
    tree_sitter.Language.build_library(
  # Store the library in the current directory
        'my-languages.so',

        # Include the Python grammar
        [
        'tree-sitter-python'
        ]
    )

buildTree()
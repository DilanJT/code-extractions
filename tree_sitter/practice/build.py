
import tree_sitter

# clone below repo in the same directory as this file
# Then run this file to generate the parser called my-languages.so
# This only needs to be done once

'git clone https://github.com/tree-sitter/tree-sitter-python'

def buildTree():
    tree_sitter.Language.build_library(
    # Store the library in the current directory
        'parser/java.so',
        # Include the Python grammar
        [
        'parser/tree-sitter-java'
        ]
    )

buildTree()

import tree_sitter


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
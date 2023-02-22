import re
from io import StringIO
import  tokenize

def remove_comments_and_docstrings(source,lang):
    if lang in ['python']:
        """
        Returns 'source' minus comments and docstrings.
        """
        io_obj = StringIO(source) 
        # StringIO is used to create a file-like object that remains in memory instead of being written to disk.

        out = ""
        prev_toktype = tokenize.INDENT
        last_lineno = -1
        last_col = 0
        for tok in tokenize.generate_tokens(io_obj.readline):
            token_type = tok[0]
            token_string = tok[1]
            start_line, start_col = tok[2]
            end_line, end_col = tok[3]
            ltext = tok[4]
            if start_line > last_lineno:
                last_col = 0
            if start_col > last_col:
                out += (" " * (start_col - last_col))
            # Remove comments:
            if token_type == tokenize.COMMENT:
                pass
            # This series of conditionals removes docstrings:
            elif token_type == tokenize.STRING:
                if prev_toktype != tokenize.INDENT:
            # This is likely a docstring; double-check we're not inside an operator:
                    if prev_toktype != tokenize.NEWLINE:
                        if start_col > 0:
                            out += token_string
            else:
                out += token_string
            prev_toktype = token_type
            last_col = end_col
            last_lineno = end_line
        temp=[]
        for x in out.split('\n'):
            if x.strip()!="":
                temp.append(x)
        return '\n'.join(temp)
    elif lang in ['ruby']:
        return source
    else:
        # https://stackoverflow.com/questions/241327/python-snippet-to-remove-c-and-c-comments
        """The purpose of this function is to be used with the re.sub() function in python's re module to replace
        certain substrings in a larger string"""
        def replacer(match):
            # retrieves the entire matched substring, which is stored in the match object
            s = match.group(0)
            # checks whether the substring starts with a forward slash (/) using the startswith() method
            if s.startswith('/'):
                return " " # note: a space and not an empty string
            else:
                return s
        """
        this function is designed to be used as a replacement function with re.sub() to remove certain substrings 
        that start with a forward slash and replace them with a space character. Any other substrings that do not 
        start with a forward slash are left unchanged.
        """

        pattern = re.compile(
            r'//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"',
            re.DOTALL | re.MULTILINE
        )
        """
        this regular expression is designed to match any of the following:
        1. any substring that starts with two forward slashes (//) and ends with a newline character
        2. any substring that starts with a forward slash and an asterisk (/*) and ends with an asterisk and a forward slash (*/)
        3. any substring that starts with a single quote (') and ends with a single quote (') and does not contain any single quotes
        4. any substring that starts with a double quote (") and ends with a double quote (") and does not contain any double quotes

        the re.DOTALL and re.MULTILINE flags are used to ensure that the regular expression matches across multiple lines

        chatgpt
        this regular expression pattern is useful for removing comments and string literals from a larger string, while leaving 
        other parts of the string intact. It can be used in combination with the re.sub() function to replace matched substrings 
        with a specified replacement string.
        """

        
        temp=[]
        for x in re.sub(pattern, replacer, source).split('\n'):
            if x.strip()!="":
                temp.append(x)
        """
        this code removes all comments and string literals from the source string, splits the resulting string into individual 
        lines, and then removes any lines that consist only of whitespace characters. The remaining non-empty lines are added 
        to the temp list, which can then be used for further processing.
        """

        return '\n'.join(temp)

"""
this function traverses the syntax tree from the root_node down to the leaf nodes, 
collecting the start and end points of each token along the way. This information 
can be used to map the tokens back to their corresponding code in the original source file.
"""
def tree_to_token_index(root_node):
    if (len(root_node.children)==0 or root_node.type=='string') and root_node.type!='comment':
        return [(root_node.start_point,root_node.end_point)]
    else:
        code_tokens=[]
        for child in root_node.children:
            code_tokens+=tree_to_token_index(child)
        return code_tokens
    
"""
tree_to_variable_index()

the function traverses the parse tree rooted at the given node and returns a list of start and
 end points for each variable identifier found in the tree.

sample code
public class HelloWorld {
    public static void main(String[] args) {
        String message = "Hello, world!";
        System.out.println(message);
    }
}

root_node = <TreeSitter node representing the entire code snippet>

index_to_code = {
    (0, 6): ('public', 'keyword'),
    (7, 12): ('class', 'keyword'),
    (13, 24): ('HelloWorld', 'class'),
    (25, 26): ('{', 'punctuation'),
    # and so on, for each token in the code
}

When tree_to_variable_index is called with root_node and index_to_code, it will traverse the parse 
tree and check if each leaf node represents a variable identifier. If a leaf node represents a 
variable identifier and its type in the parse tree matches its type in the code, tree_to_variable_index 
will not add its start and end points to the list of variable indices. Otherwise, it will add the start 
and end points of the identifier to the list. The resulting list would look like

[(47, 54), (70, 75)]

This is because the code snippet contains two variable identifiers, message and args, and 
tree_to_variable_index correctly identifies these identifiers and returns their start and 
end points in the code

"""
def tree_to_variable_index(root_node,index_to_code):
    if (len(root_node.children)==0 or root_node.type=='string') and root_node.type!='comment':
        index=(root_node.start_point,root_node.end_point)
        _,code=index_to_code[index]
        if root_node.type!=code:
            return [(root_node.start_point,root_node.end_point)]
        else:
            return []
    else:
        code_tokens=[]
        for child in root_node.children:
            code_tokens+=tree_to_variable_index(child,index_to_code)
        return code_tokens    


"""
index_to_code_token()

using same above sample java code

Suppose we want to get the token corresponding to the index (2, 18) (i.e., the token "class").
 We can pass this index along with the code snippet as a list of strings, like so:

code = [
    "public class HelloWorld {",
    "    public static void main(String[] args) {",
    "        System.out.println(\"Hello, world!\");",
    "    }",
    "}"
]
index = (0, 6)
token = index_to_code_token(index, code)
print(token)


This will output the string "public", which is the token corresponding to the given index.

"""
def index_to_code_token(index,code):
    start_point=index[0]
    end_point=index[1]
    if start_point[0]==end_point[0]:
        s=code[start_point[0]][start_point[1]:end_point[1]]
    else:
        s=""
        s+=code[start_point[0]][start_point[1]:]
        for i in range(start_point[0]+1,end_point[0]):
            s+=code[i]
        s+=code[end_point[0]][:end_point[1]]   
    return s
   
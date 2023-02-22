"""

What is a Lexeme?
- A Lexeme is a token that has been identified by the lexer.
- A Lexeme is a sequence of charachters in the source program that matches the pattern for token and is identified by the lexical
    analyzer as an instance of a token


! important !
The code below have a logical error. If you are willing fix the code you are welcome to do so.

"""

import re

# sample implementation

def tokenize(source_code):
    """Tokenize source code into a list of lexemes"""
    tokens = []

    #Define a dictionary of reserved keywords
    reserved = {
        'if': 'IF',
        'else': 'ELSE',
        'while': 'WHILE',
        'print': 'PRINT'
    }

    # Define a regular expression pattern to match identifiers
    identifier_pattern = r'[a-zA-Z_][a-zA-Z0-9_]*'

    # Loop through the input string and tokenize each lexeme
    i = 0
    while i < len(source_code):
        # Check for reserved keywords
        match = None
        for keyword, token_type in reserved.items():
            if source_code.startswith(keyword, i):
                match = keyword
                print("match", match)
                tokens.append(token_type)
                break
        
        print("tokens after checking reserved words \n", tokens)
        
        identifier = None
        # Check for identifiers
        if not match:
            match = re.match(identifier_pattern, source_code[i:])
            print("match", match)
            if match:
                identifier = match.group()
                tokens.append('IDENTIFIER:' + identifier)
        
        print("tokens after checking identifiers words \n", tokens)

        # Move the index to the end of the matched lexeme
        if identifier:
            i += len(identifier)
        else:
            # If no lexeme matched, raise an error
            print('Invalid input at position ' + str(i))
            i += 1

        # 
    
    # Return the list of tokens
    return tokens



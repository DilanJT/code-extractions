import re


def extract_tokens_pairs(input_code):

    # Define regular expression patterns for different token types
    token_patterns = [
        'identifier', r'[a-zA-Z_][a-zA-Z0-9_]*',
        'integer_literal', r'\d+',
        'float_literal', r'\d+\.\d+',
        'string_literal', r'\".*?\"',
        'operator', r'\+|\-|\*|\/|\=|\%|\^|\&|\||\~|\!|\<|\>|\?|\:|\,|\;|\(|\)|\[|\]|\{|\}',
        'whitespace', r'\s+',
        'reserved_word', r'\b(and|as|assert|async|await|break|class|continue|def|del|elif|else|except|False|finally|for|from|global|if|import|in|is|lambda|None|nonlocal|not|or|pass|raise|return|True|try|while|with|yield|print)\b'
    ]

    # Combine all patterns into a single regex pattern
    regex_pattern = '|'.join('(?P<%s>%s)' % pair for pair in zip(token_patterns[0::2], token_patterns[1::2]))
    # regex_pattern = '|'.join('(?P<%s>%s)' % pair for pair in zip(token_patterns, token_patterns))
    #print("regex_pattern", regex_pattern)

    # Tokenize the input string using the regex pattern
    # Tokenize the input string using the regex pattern
    tokens = []
    for match in re.finditer(regex_pattern, input_code):
        for name, value in match.groupdict().items():
            if value:
                tokens.append((name, value))

    return tokens

def extract_tokens(input_code):
    # Define regular expression patterns for different token types
    tokens = []
    token_pairs = extract_tokens_pairs(input_code)
    for token_pair in token_pairs:
        tokens.append(token_pair[1])

    return tokens

print("test", extract_tokens("print('Hello World!', 7)"))
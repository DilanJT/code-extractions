import re

def identifier_extractor(code_snippet):
    identifier_pattern = r'[a-zA-Z_][a-zA-Z0-9_]*'

    # Find all matches of the patterns in the code snippet
    identifiers = re.findall(identifier_pattern, code_snippet)

    return identifiers

def reserved_word_extractor(code_snippet):
    reserved_word_pattern = r'\b(and|as|assert|async|await|break|class|continue|def|del|elif|else|except|False|finally|for|from|global|if|import|in|is|lambda|None|nonlocal|not|or|pass|raise|return|True|try|while|with|yield|print)\b'

    # Find all matches of the patterns in the code snippet
    reserved_words = re.findall(reserved_word_pattern, code_snippet)

    return reserved_words




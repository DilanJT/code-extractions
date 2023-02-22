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

# java_code = """
# public class Main {
#     public static void main(String[] args) {
#         System.out.println("Hello, world!");
#     }
# }
# """

# LANGUAGE = tree_sitter.Language('parser/java.so','java')
# parser = tree_sitter.Parser()
# parser.set_language(LANGUAGE)

# singleTree = parser.parse(java_code.encode('utf-8'))
# root_node = singleTree.root_node

# print("tree to token index : ", tree_to_token_index(root_node))

#remove comments, tokenize code and extract dataflow     
def extract_dataflow(code, parser,lang):
    #remove comments
    try:
        code=remove_comments_and_docstrings(code,lang)
    except:
        pass    
    #obtain dataflow
    if lang=="php":
        code="<?php"+code+"?>"    
    try:
        tree = parser[0].parse(bytes(code,'utf8'))    
        root_node = tree.root_node  
        tokens_index=tree_to_token_index(root_node)     
        code=code.split('\n')
        code_tokens=[index_to_code_token(x,code) for x in tokens_index]  
        index_to_code={}
        for idx,(index,code) in enumerate(zip(tokens_index,code_tokens)):
            index_to_code[index]=(idx,code)  
        try:
            DFG,_=parser[1](root_node,index_to_code,{}) 
        except:
            DFG=[]
        DFG=sorted(DFG,key=lambda x:x[1])
        indexs=set()
        for d in DFG:
            if len(d[-1])!=0:
                indexs.add(d[1])
            for x in d[-1]:
                indexs.add(x)
        new_DFG=[]
        for d in DFG:
            if d[1] in indexs:
                new_DFG.append(d)
        dfg=new_DFG
    except:
        dfg=[]
    return code_tokens,dfg
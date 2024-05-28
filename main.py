import sys
from antlr4 import *
from Python3Lexer import Python3Lexer
from Python3Parser import Python3Parser
from Python3ParserVisitor import Python3ParserVisitor

from utils import print_tree, format_cpp_code

def main(argv):
    input_code = ''''''
    with open(argv[1], 'r') as f:
        input_code = f.read()

    input_stream = InputStream(input_code)
    lexer = Python3Lexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = Python3Parser(stream)
    
    tree = parser.file_input()

    print_tree(tree, parser)    

    visitor = Python3ParserVisitor()
    output_code = visitor.visit(tree)
    
    output_code = format_cpp_code(output_code)
    
    print(f"\nOUTPUT:\n{output_code}")
    

def convert_code(input_code: str):
    input_stream = InputStream(input_code)
    lexer = Python3Lexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = Python3Parser(stream)
    
    tree = parser.file_input()

    visitor = Python3ParserVisitor()
    output_code = visitor.visit(tree)
    
    output_code = format_cpp_code(output_code)
    
    return output_code

if __name__ == "__main__":
    main(sys.argv)
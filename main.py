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

    lines = output_code.split("\n")
    output_code = ""
    indent = 0
    for line in lines:
        line = line.strip()

        if line.startswith("}"):
            indent -= 1
        output_code += "\t" * indent + line + "\n"
        if line.endswith("{"):
            indent += 1

    with open(argv[2], "w") as f:
        f.write(output_code)
        f.close()

if __name__ == "__main__":
    main(sys.argv)
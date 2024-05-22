from antlr4 import *
from Python3Lexer import Python3Lexer
from Python3Parser import Python3Parser
from Python3ParserVisitor import Python3ParserVisitor

def main():
    input_code = """a += 3 \n"""

    input_stream = InputStream(input_code)
    lexer = Python3Lexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = Python3Parser(stream)

    tree = parser.single_input()
    print(tree.toStringTree(recog=parser))

    visitor = Python3ParserVisitor()
    print(visitor.visit(tree))

if __name__ == "__main__":
    main()

from antlr4 import *
from CLexer import CLexer
from CParser import CParser
from semantic import semanticVisitor
import sys 
CFile = "/Users/kni/projects/spring/parser/test/t6.c"




def lexerize(filePath): 
    input_stream = FileStream(filePath)
    lexer = CLexer(input_stream)
    token_stream = CommonTokenStream(lexer)

    # print tokens in the form of raw text 
    token_stream_text = token_stream.getText()
    print("Token Stream Text:", token_stream_text)
    # print tokens in the form of table 
    print("{:<10} {:<20} {:<15} {:<15}".format("Token Type", "Text", "Line", "Column")) 
    print("="*60) 

    for token in token_stream.tokens:
        print("{:<10} {:<20} {:<15} {:<15}".format(
            CLexer.symbolicNames[token.type], 
            token.text, 
            token.line, 
            token.column
            ))
    return token_stream


if __name__ == "__main__": 
    if len(sys.argv) > 1: 
        CFile = sys.argv[1]
    print(f"test files: {CFile}") 
    token_stream = lexerize(CFile)
    print("[ok] lexel analysis done ")
    parser = CParser(token_stream)
    tree = parser.program()

    semanticAnalizer = semanticVisitor() 
    semanticAnalizer.visit(tree)
    semanticAnalizer.save(CFile.split('.')[0] + ".ll")
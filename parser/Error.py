from antlr4.error.ErrorListener import ErrorListener 
from antlr4 import * 

class SemanticError(Exception): 
    """
    sementic errors to be raised when detecting a semantic error 
    """
    def __init__(self, msg, ctx=None): 
        super().__init__() 
        if ctx: 
            self.line = ctx.start.line
            self.column = ctx.start.column
        else: 
            self.line = 0 
            self.column = 0
        self.msg = msg 
    
    def __str__(self): 
        return "[Semantic Error] " + str(self.line) + ":" + str(self.column) + " " + self.msg
    

class syntaxErrorListener(ErrorListener): 

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        print(f"[SyntaxError] line[{line}] column[{column}] : ", msg)
# Generated from CParser.g4 by ANTLR 4.13.1
from antlr4 import *
if "." in __name__:
    from .CParser import CParser
else:
    from CParser import CParser

# This class defines a complete generic visitor for a parse tree produced by CParser.

class CParserVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by CParser#program.
    def visitProgram(self, ctx:CParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#function.
    def visitFunction(self, ctx:CParser.FunctionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#var_type.
    def visitVar_type(self, ctx:CParser.Var_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#formal_args.
    def visitFormal_args(self, ctx:CParser.Formal_argsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#actual_args.
    def visitActual_args(self, ctx:CParser.Actual_argsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#statement.
    def visitStatement(self, ctx:CParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#return_statm.
    def visitReturn_statm(self, ctx:CParser.Return_statmContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#declare_var_statm.
    def visitDeclare_var_statm(self, ctx:CParser.Declare_var_statmContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#assign_statm.
    def visitAssign_statm(self, ctx:CParser.Assign_statmContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#call_func_statm.
    def visitCall_func_statm(self, ctx:CParser.Call_func_statmContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#condition_statm.
    def visitCondition_statm(self, ctx:CParser.Condition_statmContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#while_statm.
    def visitWhile_statm(self, ctx:CParser.While_statmContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#for_statm.
    def visitFor_statm(self, ctx:CParser.For_statmContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#arith_statm.
    def visitArith_statm(self, ctx:CParser.Arith_statmContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#const_val.
    def visitConst_val(self, ctx:CParser.Const_valContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#eval_expr.
    def visitEval_expr(self, ctx:CParser.Eval_exprContext):
        return self.visitChildren(ctx)



del CParser
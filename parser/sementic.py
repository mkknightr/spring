from CParserVisitor import CParserVisitor
from antlr4 import *
if "." in __name__:
    from .CParser import CParser
else:
    from CParser import CParser


class sementicVisitor(CParserVisitor): 

    # Visit a parse tree produced by CParser#program.
    def visitProgram(self, ctx:CParser.ProgramContext):
        print("---- VISIT Program ----")
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#function.
    def visitFunction(self, ctx:CParser.FunctionContext):
        print("---- VISIT Function ----") 
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#var_type.
    def visitVar_type(self, ctx:CParser.Var_typeContext):
        print("---- VISIT Var_type ----") 
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#formal_args.
    def visitFormal_args(self, ctx:CParser.Formal_argsContext):
        print("---- VISIT Formal_args ----") 
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#actual_args.
    def visitActual_args(self, ctx:CParser.Actual_argsContext):
        print("---- VISIT Actual_args ----") 
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#statement.
    def visitStatement(self, ctx:CParser.StatementContext):
        print("---- VISIT Statement ----") 
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#return_statm.
    def visitReturn_statm(self, ctx:CParser.Return_statmContext):
        print("---- VISIT Return_statm ----") 
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#declare_var_statm.
    def visitDeclare_var_statm(self, ctx:CParser.Declare_var_statmContext):
        print("---- VISIT Declare_var_statm ----") 
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#assign_statm.
    def visitAssign_statm(self, ctx:CParser.Assign_statmContext):
        print("---- VISIT Assign_statm ----") 
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#call_func_statm.
    def visitCall_func_statm(self, ctx:CParser.Call_func_statmContext):
        print("---- VISIT Call_func_statm ----") 
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#condition_statm.
    def visitCondition_statm(self, ctx:CParser.Condition_statmContext):
        print("---- VISIT Condition_statm ----") 
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#while_statm.
    def visitWhile_statm(self, ctx:CParser.While_statmContext):
        print("---- VISIT While_statm ----") 
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#for_statm.
    def visitFor_statm(self, ctx:CParser.For_statmContext):
        print("---- VISIT For_statm ----") 
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#arith_statm.
    def visitArith_statm(self, ctx:CParser.Arith_statmContext):
        print("---- VISIT Arith_statm ----") 
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#const_val.
    def visitConst_val(self, ctx:CParser.Const_valContext):
        print("---- VISIT Const_val ----") 
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#eval_expr.
    def visitEval_expr(self, ctx:CParser.Eval_exprContext):
        print("---- VISIT Eval_expr ----") 
        return self.visitChildren(ctx)

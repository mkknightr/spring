# Generated from CParser.g4 by ANTLR 4.13.1
from antlr4 import *
if "." in __name__:
    from .CParser import CParser
else:
    from CParser import CParser

# This class defines a complete listener for a parse tree produced by CParser.
class CParserListener(ParseTreeListener):

    # Enter a parse tree produced by CParser#program.
    def enterProgram(self, ctx:CParser.ProgramContext):
        pass

    # Exit a parse tree produced by CParser#program.
    def exitProgram(self, ctx:CParser.ProgramContext):
        pass


    # Enter a parse tree produced by CParser#function.
    def enterFunction(self, ctx:CParser.FunctionContext):
        pass

    # Exit a parse tree produced by CParser#function.
    def exitFunction(self, ctx:CParser.FunctionContext):
        pass


    # Enter a parse tree produced by CParser#var_type.
    def enterVar_type(self, ctx:CParser.Var_typeContext):
        pass

    # Exit a parse tree produced by CParser#var_type.
    def exitVar_type(self, ctx:CParser.Var_typeContext):
        pass


    # Enter a parse tree produced by CParser#formal_args.
    def enterFormal_args(self, ctx:CParser.Formal_argsContext):
        pass

    # Exit a parse tree produced by CParser#formal_args.
    def exitFormal_args(self, ctx:CParser.Formal_argsContext):
        pass


    # Enter a parse tree produced by CParser#actual_args.
    def enterActual_args(self, ctx:CParser.Actual_argsContext):
        pass

    # Exit a parse tree produced by CParser#actual_args.
    def exitActual_args(self, ctx:CParser.Actual_argsContext):
        pass


    # Enter a parse tree produced by CParser#statement.
    def enterStatement(self, ctx:CParser.StatementContext):
        pass

    # Exit a parse tree produced by CParser#statement.
    def exitStatement(self, ctx:CParser.StatementContext):
        pass


    # Enter a parse tree produced by CParser#return_statm.
    def enterReturn_statm(self, ctx:CParser.Return_statmContext):
        pass

    # Exit a parse tree produced by CParser#return_statm.
    def exitReturn_statm(self, ctx:CParser.Return_statmContext):
        pass


    # Enter a parse tree produced by CParser#declare_var_statm.
    def enterDeclare_var_statm(self, ctx:CParser.Declare_var_statmContext):
        pass

    # Exit a parse tree produced by CParser#declare_var_statm.
    def exitDeclare_var_statm(self, ctx:CParser.Declare_var_statmContext):
        pass


    # Enter a parse tree produced by CParser#assign_statm.
    def enterAssign_statm(self, ctx:CParser.Assign_statmContext):
        pass

    # Exit a parse tree produced by CParser#assign_statm.
    def exitAssign_statm(self, ctx:CParser.Assign_statmContext):
        pass


    # Enter a parse tree produced by CParser#call_func_statm.
    def enterCall_func_statm(self, ctx:CParser.Call_func_statmContext):
        pass

    # Exit a parse tree produced by CParser#call_func_statm.
    def exitCall_func_statm(self, ctx:CParser.Call_func_statmContext):
        pass


    # Enter a parse tree produced by CParser#condition_statm.
    def enterCondition_statm(self, ctx:CParser.Condition_statmContext):
        pass

    # Exit a parse tree produced by CParser#condition_statm.
    def exitCondition_statm(self, ctx:CParser.Condition_statmContext):
        pass


    # Enter a parse tree produced by CParser#while_statm.
    def enterWhile_statm(self, ctx:CParser.While_statmContext):
        pass

    # Exit a parse tree produced by CParser#while_statm.
    def exitWhile_statm(self, ctx:CParser.While_statmContext):
        pass


    # Enter a parse tree produced by CParser#for_statm.
    def enterFor_statm(self, ctx:CParser.For_statmContext):
        pass

    # Exit a parse tree produced by CParser#for_statm.
    def exitFor_statm(self, ctx:CParser.For_statmContext):
        pass


    # Enter a parse tree produced by CParser#arith_statm.
    def enterArith_statm(self, ctx:CParser.Arith_statmContext):
        pass

    # Exit a parse tree produced by CParser#arith_statm.
    def exitArith_statm(self, ctx:CParser.Arith_statmContext):
        pass


    # Enter a parse tree produced by CParser#const_val.
    def enterConst_val(self, ctx:CParser.Const_valContext):
        pass

    # Exit a parse tree produced by CParser#const_val.
    def exitConst_val(self, ctx:CParser.Const_valContext):
        pass


    # Enter a parse tree produced by CParser#eval_expr.
    def enterEval_expr(self, ctx:CParser.Eval_exprContext):
        pass

    # Exit a parse tree produced by CParser#eval_expr.
    def exitEval_expr(self, ctx:CParser.Eval_exprContext):
        pass



del CParser
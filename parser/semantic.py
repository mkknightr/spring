from CParserVisitor import CParserVisitor
from CLexer import CLexer
from llvmlite import ir 
from antlr4 import *
from config import Configuration
from symbolTable import SymbolTable
from Error import SemanticError

if "." in __name__:
    from .CParser import CParser
else:
    from CParser import CParser

# variable type setup 
float_t = ir.FloatType() 
int32_t = ir.IntType(32)
int8_t = ir.IntType(8)
void_t = ir.VoidType()


# function type setup 
printf_function_type = ir.FunctionType(int32_t, [int8_t.as_pointer()], var_arg=True)

class semanticVisitor(CParserVisitor): 

    def __init__(self) -> None:
        super().__init__()

        ## llvm configuration set up 
        self.Module = ir.Module()
        self.Module.triple = Configuration.LLVM_TRIPLE_MACOS
        self.Module.data_layout =  Configuration.LLVM_DATA_LAYOUT

        self.Blocks = [] 
        self.Builders = [] 
        self.Functions = dict() 

        self.m_cur_function = '' 
        self.m_state = 0 

        self.m_symblol_table = SymbolTable()
        self.Constant = -1; 

    def getConstantIndex(self):
        self.Constant += 1 
        return self.Constant



    # Visit a parse tree produced by CParser#program.
    def visitProgram(self, ctx:CParser.ProgramContext):
        print("---- VISIT Program ----")
        """
        program : function+;
        """
        self.m_symblol_table.display()
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#function.
    def visitFunction(self, ctx:CParser.FunctionContext):
        print("---- VISIT Function ----") 
        """   
        function : var_type ID LPAREN formal_args? RPAREN LBRACE statement* RBRACE;
        """
        self.m_symblol_table.display() 

        # get the return type 
        return_type = self.visit(ctx.getChild(0))
        if return_type == "": 
            raise SemanticError(ctx=ctx, msg="Unexpedted function type error") 
        # get the function name  
        function_name = ctx.getChild(1).getText()
        # get the function formal arguments  
        if ctx.getChild(3).getText() != ")":
            formal_arguments = self.visit(ctx.getChild(3))
        else: 
            formal_arguments = [] 
        # get the function arguments type list   
        args_type_list = [] 
        for i in range(len(formal_arguments)):
            args_type_list.append(formal_arguments[i]['type'])
        # create the function type according to return value type and args type list 
        llvmFunctionType = ir.FunctionType(return_type, args_type_list)
        # bind the function with module and name 
        llvmFunction = ir.Function(self.Module, llvmFunctionType, name=function_name)
        
        # 将llvm中的变量名字改为C语言程序中的变量名
        for i in range(len(formal_arguments)): 
            llvmFunction.args[i].name = formal_arguments[i]['name']
        
        # 开始构建函数体
        functionBlock = llvmFunction.append_basic_block(name=function_name + '.entry') 
        if function_name in self.Functions: 
            raise SemanticError(ctx=ctx, msg=f"Redefinition of function {function_name}")
        else: 
            self.Functions[function_name] = llvmFunction
        functionBuilder = ir.IRBuilder(functionBlock)
        
        # 将当前函数体和函数构造器设置为self visitor的最后一个值
        self.Blocks.append(functionBlock)
        self.Builders.append(functionBuilder)

        self.m_cur_function = function_name
        self.m_symblol_table.EnterScope() 

        for i in range(len(formal_arguments)): 
            var_new = functionBuilder.alloca(formal_arguments[i]['type'])
            functionBuilder.store(llvmFunction.args[i], var_new)
            i_var = {} 
            i_var['type'] = formal_arguments[i]['type'] 
            i_var['name'] = var_new
            add_item_result = self.m_symblol_table.AddItem(formal_arguments[i]['name'], i_var)
            if add_item_result != "ok":
                raise SemanticError(ctx=ctx, msg=add_item_result)

        for i in range(ctx.getChildCount()): 
            i_child = ctx.getChild(i)
            if isinstance(i_child, CParser.StatementContext): 
                self.visit(i_child)
        self.m_cur_function = ''
        self.Blocks.pop() 
        self.Builders.pop() 
        self.m_symblol_table.QuitScope()

        print(f"Function processed done [{function_name}]")
        print(str(llvmFunction))

        return 


    # Visit a parse tree produced by CParser#var_type.
    def visitVar_type(self, ctx:CParser.Var_typeContext):
        print("---- VISIT Var_type ----") 
        """
        var_type : INT_TYPE|FLOAT_TYPE|CHAR_TYPE|VOID_TYPE
        """
        global float_t, int32_t, int8_t, void_t
        if ctx.getText() == 'int': 
            return int32_t
        elif ctx.getText() == "float": 
            return float_t
        elif ctx.getText() == "char": 
            return int8_t
        elif ctx.getText() == "void": 
            return void_t
        else: 
            return ""


    # Visit a parse tree produced by CParser#formal_args.
    def visitFormal_args(self, ctx:CParser.Formal_argsContext):
        print("---- VISIT Formal_args ----") 
        """
        formal_args : (var_type (MULTIPLY)? ID ( LBRACK (INT)? RBRACK)? ) (COMMA var_type (MULTIPLY)? ID ( LBRACK (INT)? RBRACK)? )*;
        """
        params_list = []
        child_count = ctx.getChildCount() 
        for i in range(child_count): 
            i_child = ctx.getChild(i)
            if isinstance(i_child, CParser.Var_typeContext): 
                i_type = self.visit(i_child)
                i_id = ctx.getChild(i + 1).getText()
                params_list.append({'type': i_type, 'name': i_id})
        print(params_list)
        return params_list


    # Visit a parse tree produced by CParser#actual_args.
    def visitActual_args(self, ctx:CParser.Actual_argsContext):
        print("---- VISIT Actual_args ----")
        """
        actual_args : (eval_expr) ( COMMA eval_expr)*; 
        """

        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#statement.
    def visitStatement(self, ctx:CParser.StatementContext):
        print("---- VISIT Statement ----") 
        """
        statement : 
            declare_var_statm SEMI | 
            assign_statm SEMI | 
            return_statm SEMI | 
            call_func_statm SEMI | 
            condition_statm | 
            while_statm | 
            for_statm | 
            arith_statm SEMI
            """
        
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#return_statm.
    def visitReturn_statm(self, ctx:CParser.Return_statmContext):
        print("---- VISIT Return_statm ----") 
        """
        return_statm : RET | RET ( eval_expr )
        """
        self.m_symblol_table.display()
        if ctx.getChildCount() == 1: 
            self.Builders[-1].ret_void()
            return f"function {self.m_cur_function} return void "
        else: 
            return_value = self.visit(ctx.getChild(1))
            self.Builders[-1].ret(return_value)
            return f"function {self.m_cur_function} return {return_value}"

    # Visit a parse tree produced by CParser#declare_var_statm.
    def visitDeclare_var_statm(self, ctx:CParser.Declare_var_statmContext):
        print("---- VISIT Declare_var_statm ----") 
        """
        declare_var_statm : 
        var_type (MULTIPLY)? ID |       
        var_type (MULTIPLY)? ID LBRACK ( eval_expr ) RBRACK |      
        var_type (MULTIPLY)? ID ASSIGN ( eval_expr ) 
        """
        var_type = self.visit(ctx.getChild(0))
        if ctx.getChild(1).getText() != "*":
            var_id = ctx.getChild(1).getText() 
            if self.m_symblol_table.InGlobalScope(): 
                llvmVar = ir.GlobalVariable(self.Module, var_type, name=var_id)
                llvmVar.linkage = 'internal'
            else: 
                llvmBuiler = self.Builders[-1] 
                llvmVar = llvmBuiler.alloca(var_type, name=var_id)
            symbolVar = {} 
            symbolVar["type"] = var_type
            symbolVar["name"] = llvmVar
            add_item_result = self.m_symblol_table.AddItem(var_id, symbolVar)
            if add_item_result != "ok": 
                raise SemanticError(msg=f"failed to add variable {var_id} to symbol table")
            if ctx.getChild(2).getText() == "=":
                var_value = self.visit(ctx.getChild(3))
                if self.m_symblol_table.InGlobalScope():
                    llvmVar.initializer = ir.Constant(var_value['type'], var_value['name'].constant)
                else: 
                    # TODO 在这里后续可以拓展关于强制类型转换的内容
                    if var_type != var_value.type:
                        raise SemanticError(msg=f"varibale type mismatches in assignment statement",ctx=ctx)
                    else: 
                        llvmVar.initializer = var_value
                return 
            elif ctx.getChild(2).getText() == "[": 
                #TODO 在这里可以拓展初始化数组变量 目前暂时并不支持
                pass
            else: 
                raise SemanticError(msg=Configuration.ERROR_UPEXPECTED, ctx=ctx) 
        else: 
            # TODO 在这里后续可以拓展关于指针类型的内容，目前暂时不支持
            pass
        return 

    # Visit a parse tree produced by CParser#assign_statm.
    def visitAssign_statm(self, ctx:CParser.Assign_statmContext):
        print("---- VISIT Assign_statm ----") 
        """
        assign_statm : eval_expr ASSIGN ( eval_expr );
        """
        llvmBuiler = self.Builders[-1]
        var_id = ctx.getChild(0).getText() 
        if self.m_symblol_table.exist(var_id): 
            var_value = self.visit(ctx.getChild(2))
            llvmVar = self.m_symblol_table.GetItem(var_id)
            llvmBuiler.store(var_value['name'], llvmVar)
        else: 
            raise SemanticError(msg=f"Cannot detect definition for variable {var_id}", ctx=ctx)
        return ir.Constant(var_value)


    # Visit a parse tree produced by CParser#call_func_statm.
    def visitCall_func_statm(self, ctx:CParser.Call_func_statmContext):
        print("---- VISIT Call_func_statm ----") 
        """
        call_func_statm : ID LPAREN ( actual_args? ) RPAREN;
        """
        self.m_symblol_table.display() 
        if ctx.getChild(0).getText() == "printf": 
            if 'printf' in self.Functions: 
                printf = self.Functions['printf']
            else:   
                printf = ir.Function(self.Module, printf_function_type, name="printf")
                self.Functions['printf'] = printf 
            if ctx.getChild(2).getText() != ")": 
                printf_str = self.visit(ctx.getChild(2))
                # Call printf to print the string
                self.Builders[-1].call(printf, [printf_str.gep([ir.Constant(int32_t, 0),
                                    ir.Constant(int32_t, 0)])])
                return f"call function statement called printf function"
            else: 
                raise SemanticError(msg="printf function calling should have argument at least one", ctx=ctx)
        # TODO: 这里可以增加更多的库函数调用如scanf, strlen等等
        else:
            function_name = ctx.getChild(0).getText()
            if function_name in self.Functions: 
                # TODO : call the function and pass the actual_args 
                pass
            else: 
                raise SemanticError(msg=f"Undefined function {function_name}", ctx=ctx); 
            return

    # Visit a parse tree produced by CParser#condition_statm.
    def visitCondition_statm(self, ctx:CParser.Condition_statmContext):
        print("---- VISIT Condition_statm ----") 
        """
        condition_statm : 
            IF LPAREN ( eval_expr ) RPAREN 
                LBRACE statement* RBRACE
            ( ELSE IF LPAREN ( eval_expr ) RPAREN 
                LBRACE statement* RBRACE 
            )*
            ( ELSE LBRACE statement* RBRACE )?
        """
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#while_statm.
    def visitWhile_statm(self, ctx:CParser.While_statmContext):
        print("---- VISIT While_statm ----")
        """
        WHILE LPAREN ( eval_expr ) RPAREN 
        LBRACE 
            statement* 
        RBRACE
        """
        self.m_symblol_table.EnterScope() 
        llvmBuiler = self.Builders[-1]
        while_statm_condition = llvmBuiler.append_basic_block()
        while_statm_body = llvmBuiler.append_basic_block() 
        while_statm_end = llvmBuiler.append_basic_block() 

        llvmBuiler.branch(while_statm_condition)
        self.Blocks.pop()
        self.Builders.pop()
        self.Blocks.append(while_statm_condition)
        self.Builders.append(ir.IRBuilder(while_statm_condition))

        condition_result = self.visit(ctx.getChild(2))
        self.Builders[-1].cbranch(condition_result['name'], while_statm_body, while_statm_end)

        self.Blocks.pop()
        self.Builders.pop()
        self.Blocks.append(while_statm_body)
        self.Builders.append(ir.IRBuilder(while_statm_body))


        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#for_statm.
    def visitFor_statm(self, ctx:CParser.For_statmContext):
        print("---- VISIT For_statm ----") 
        """
        for_statm : 
        FOR LPAREN ( declare_var_statm | assign_statm )? 
            SEMI eval_expr? 
            SEMI ( assign_statm | arith_statm )? RPAREN 
        LBRACE
            statement*
        RBRACE
        感觉这里会是比较复杂的逻辑所在
        """
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#arith_statm.
    def visitArith_statm(self, ctx:CParser.Arith_statmContext):
        print("---- VISIT Arith_statm ----") 
        """
        arith_statm : 
        eval_expr SELF_INC | 
        eval_expr SELF_DEC | 
        SELF_INC eval_expr | 
        SELF_DEC eval_expr | 
        eval_expr SHL eval_expr |   
        eval_expr SHR eval_expr
        对涉及到的表达式进行对应的计算
        这里的语法规则和eval_expr的语法规则可能稍微有点重复了
        """
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#const_val.
    def visitConst_val(self, ctx:CParser.Const_valContext):
        print("---- VISIT Const_val ----")
        """
        const_val : INT | FLOAT | CHAR | STRING | ESCAPE_CHAR
        返回对应的常量值
        """
        const_type =  ctx.getChild(0).getSymbol().type
        if const_type == CLexer.INT: 
            return ir.Constant(int32_t, int(ctx.getText()))
        elif const_type == CLexer.STRING: 
            string_literal = ctx.getText().replace('\\n', '\n') # some quit bothering problem 
            normalized_string = string_literal[1:-1] # throw the ""
            normalized_string += '\0' # null terminated 
            ir_string = ir.GlobalVariable(self.Module, ir.ArrayType(int8_t, len(normalized_string)),
                                             name=".str%d"%(self.getConstantIndex()))
            ir_string.linkage = 'internal'
            ir_string.global_constant = True
            ir_string.initializer = ir.Constant(ir.ArrayType(int8_t,  len(normalized_string)),
                                    bytearray(normalized_string, 'utf-8'))
            return ir_string
        elif const_type == CLexer.FLOAT: 
            return ir.Constant(float_t, float(ctx.getText()))
        elif const_type == CLexer.CHAR: 
            return ir.Constant(int8_t, ctx.getText()[0])
        elif const_type == CLexer.ESCAPE_CHAR: 
            return ir.Constant(int8_t, ctx.getText()[0]) 
        else: 
            raise SemanticError(msg="! Unexpected error when analizing const_val ")


    # Visit a parse tree produced by CParser#eval_expr.
    def visitEval_expr(self, ctx:CParser.Eval_exprContext):
        print("---- VISIT Eval_expr ----") 
        """
        关于此处的大概逻辑和返回值说明
        具值表达式：也就是表达式具有特定的值。
        如果表达式涉及到函数调用和数据写入，那么在完成相关的对于符号表活着变量的修改之后，返回表达式的值即可
        如果不涉及到数据的写操作而只是计算的话，只返回值即可
        """
        return self.visitChildren(ctx)
    def save(self, filename): 
        """
        save the IR code to file 
        """
        with open(filename, "w") as f: 
            f.write(repr(self.Module))
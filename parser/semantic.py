from CParserVisitor import CParserVisitor
from CLexer import CLexer
from llvmlite import ir 
from antlr4 import *
from config import Configuration, ExprType
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
        formal_args : 
            (var_type (MULTIPLY)? ID ( LBRACK (INT)? RBRACK)? ) 
            (COMMA var_type (MULTIPLY)? ID ( LBRACK (INT)? RBRACK)? )*;
        
        TODO: 这里还需要增加对【指针类型】和【数组类型】的支持
        """
        params_list = []
        child_count = ctx.getChildCount() 
        for i in range(child_count): 
            i_child = ctx.getChild(i)
            if isinstance(i_child, CParser.Var_typeContext): 
                i_type = self.visit(i_child)
                if (i + 1) < child_count and ctx.getChild(i + 1).getText() == "*": 
                    i_id = ctx.getChild(i + 2).getText()
                    params_list.append({'type': i_type.as_pointer(), 'name': i_id})
                    i += 2
                elif (i + 2) < child_count and ctx.getChild(i + 2).getText() == "[":
                    i_id = ctx.getChild(i + 1).getText()
                    params_list.append({"type": ir.types.ArrayType(i_type, 1000), 'name': i_id})
                    i += 2
                else: 
                    i_id = ctx.getChild(i + 1).getText()
                    params_list.append({'type': i_type, 'name': i_id})
                    i+= 1
        print(params_list)
        return params_list


    # Visit a parse tree produced by CParser#actual_args.
    def visitActual_args(self, ctx:CParser.Actual_argsContext):
        print("---- VISIT Actual_args ----")
        """
        actual_args : 
            (eval_expr) ( COMMA eval_expr)*; 

        """
        llvmBuiler = self.Builders[-1]
        actual_args_list = [] 
        for i in range(ctx.getChildCount()): 
            i_child = ctx.getChild(i)
            if isinstance(i_child, CParser.Eval_exprContext):
                return_set = self.visit(i_child)
                if return_set['meta'] == ExprType.CONST_EXPR: 
                    actual_args_list.append(return_set['value'])
                else: 
                    value = llvmBuiler.load(return_set['value'])
                    actual_args_list.append(value)
        return actual_args_list


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
            self.Builders[-1].ret(return_value['value'])
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
            if ctx.getChildCount() < 3 or ctx.getChild(2).getText() == "=" : 
                if self.m_symblol_table.InGlobalScope(): 
                    # TODO 本次不涉及到全局变量 暂时搁置
                    return
                else: 
                    llvmBuiler = self.Builders[-1] 
                    llvmVar = llvmBuiler.alloca(var_type, name=var_id)
                symbolVar = {} 
                symbolVar["type"] = var_type
                symbolVar["name"] = llvmVar
                add_item_result = self.m_symblol_table.AddItem(var_id, symbolVar)
                if add_item_result != "ok": 
                    raise SemanticError(msg=f"failed to add variable {var_id} to symbol table")
                if ctx.getChildCount() < 3: 
                    return
                elif ctx.getChild(2).getText() == "=":
                    return_set = self.visit(ctx.getChild(3))
                    return_value = return_set['value']
                    if return_set['meta'] == ExprType.CONST_EXPR or return_set['meta'] == ExprType.VAR_EXPR: 
                        value = return_value
                    else: 
                        value = llvmBuiler.load(return_value)
                    if self.m_symblol_table.InGlobalScope():
                        # TODO: 本次并不会涉及到全局变量 暂时搁置
                        return
                    else: 
                        # TODO 在这里后续可以拓展关于强制类型转换的内容
                        if var_type != value.type:
                            raise SemanticError(msg=f"varibale type mismatches in assignment statement",ctx=ctx)
                        else: 
                            llvmBuiler.store(value, llvmVar)
                            return
                else: 
                    raise SemanticError(msg=f"Unexpected error", ctx=ctx)     
            elif ctx.getChild(2).getText() == "[": 
                array_size = int(ctx.getChild(3).getText())
                array_type = ir.ArrayType(var_type, array_size)
                llvmBuiler = self.Builders[-1]
                llvmVar = llvmBuiler.alloca(array_type, name=f"{var_id}.array")
                symbolVar = {} 
                symbolVar["type"] = array_type
                symbolVar["name"] = llvmVar
                add_item_result = self.m_symblol_table.AddItem(var_id, symbolVar)
                if add_item_result != "ok": 
                    raise SemanticError(msg=f"failed to add variable {var_id} to symbol table")
                return
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
        left = self.visit(ctx.getChild(0))
        right = self.visit(ctx.getChild(2))
        if right['meta'] == ExprType.CONST_EXPR or right['meta'] == ExprType.VAR_EXPR: 
            right_value = right['value'] 
        else: 
            right_value = llvmBuiler.load(right['value'])

        if left['meta'] == ExprType.CONST_EXPR: 
            raise SemanticError(msg=f"assign object mush be a left value, {ctx.getChild(0).getText()} can not", ctx=ctx)
        llvmBuiler.store(right_value, left['value']) 
        
        return


    # Visit a parse tree produced by CParser#call_func_statm.
    def visitCall_func_statm(self, ctx:CParser.Call_func_statmContext):
        print("---- VISIT Call_func_statm ----") 
        """
        call_func_statm : ID LPAREN ( actual_args? ) RPAREN;
        【期待】actual_args的visitor节点返回参数列表
        【返回】返回函数调用的返回值
        TODO: 这里可以增加更多的库函数调用
        """
        self.m_symblol_table.display() 
        if ctx.getChild(0).getText() == "printf": 
            if 'printf' in self.Functions: 
                printf = self.Functions['printf']
            else:   
                printf = ir.Function(self.Module, printf_function_type, name="printf")
                self.Functions['printf'] = printf 
            if ctx.getChild(2).getText() != ")": 
                args_list = self.visit(ctx.getChild(2))
                self.Builders[-1].call(printf, args_list)
                return f"call function statement called printf function"
            else: 
                raise SemanticError(msg="printf function calling should have argument at least one", ctx=ctx)
        # TODO: 这里可以增加更多的库函数调用如scanf, strlen等等
        else:
            function_name = ctx.getChild(0).getText()
            if function_name in self.Functions: 
                llvmFunction = self.Functions[function_name]
                parameter_list = []
                if ctx.getChild(2).getText() != ")": 
                    parameter_list = self.visit(ctx.getChild(2))
                llvmReturnValue = self.Builders[-1].call(llvmFunction, parameter_list)
                return llvmReturnValue
            else: 
                raise SemanticError(msg=f"Undefined function {function_name}", ctx=ctx); 

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

        
    
        
        num_of_else_if = 0
        pos_of_else_if_evalstmt = []
        has_else = False

        # 首先判断有多少个else if， 然后判断有没有else
        for i in range(0, ctx.getChildCount()-1):
            leftChild = ctx.getChild(i)
            rightChild = ctx.getChild(i+1)
            if leftChild.getText() == "else" and rightChild.getText() == "if":
                num_of_else_if += 1
                pos_of_else_if_evalstmt.append(i + 3)
                print("[debug] catch else if")
            elif leftChild.getText() == "else" and not rightChild.getText() == "if":
                has_else = True
                print("[debug] catch else")


        parse_child_count = 0

        self.m_symblol_table.EnterScope()
        llvmBuilder = self.Builders[-1]

        if_body_block = llvmBuilder.append_basic_block()  # 条件为真执行的语句块
        else_if_body_block = [] # else if为真语句块
        for i in range(0, num_of_else_if):
            else_if_body_block.append(llvmBuilder.append_basic_block())
        else_body_block = llvmBuilder.append_basic_block() if has_else else None  # else 执行语句
        end_block = llvmBuilder.append_basic_block()  # 最终结束块
        
        
        # 分支判断

        
        else_if_blocks = [llvmBuilder.append_basic_block(f"else_if_{i}") for i in range(num_of_else_if)]

        # 处理 if判断
        condition_result = self.visit(ctx.getChild(2))  # eval_expr 的结果
        llvmBuilder.cbranch(condition_result, if_body_block, else_if_blocks[0] if num_of_else_if > 0 else (else_body_block if has_else else end_block))
        
        # 处理else if判断
        for i in range(num_of_else_if):
            self.Blocks.pop()
            self.Builders.pop()

            self.Blocks.append(else_if_blocks[i])
            self.Builders.append(ir.IRBuilder(else_if_blocks[i]))

            llvmBuilder = self.Builders[-1]

            e_condition_result = self.visit(ctx.getChild(pos_of_else_if_evalstmt[i]))
            next_block = else_if_blocks[i + 1] if i + 1 < num_of_else_if else (else_body_block if has_else else end_block)
            llvmBuilder.cbranch(e_condition_result, else_if_body_block[i], next_block)

            



        # 进入 if 语句块
        self.Blocks.pop()
        self.Builders.pop()
        self.Blocks.append(if_body_block)
        self.Builders.append(ir.IRBuilder(if_body_block))
        
        for i in range(parse_child_count, ctx.getChildCount()):  # 注意只处理if里面的statement
            if ctx.getChild(i).getText() == "}":
                parse_child_count = i + 1
                break

            if isinstance(ctx.getChild(i), CParser.StatementContext):
                self.visit(ctx.getChild(i))

        self.Builders[-1].branch(end_block)  # 跳转到最终结束块


        # 处理 else if 语句块
        for i, elif_body_block in enumerate(else_if_body_block):
                
            self.Blocks.pop()
            self.Builders.pop()
            self.Blocks.append(elif_body_block)
            self.Builders.append(ir.IRBuilder(elif_body_block))

            for i in range(parse_child_count, ctx.getChildCount()):  # 注意只处理if里面的statement
                if ctx.getChild(i).getText() == "}":
                    parse_child_count = i + 1
                    break

                if isinstance(ctx.getChild(i), CParser.StatementContext):
                    self.visit(ctx.getChild(i))

            self.Builders[-1].branch(end_block)  # 跳转到最终结束块


        # 处理else 语句块
        if has_else:
            self.Blocks.pop()
            self.Builders.pop()
            self.Blocks.append(else_body_block)
            self.Builders.append(ir.IRBuilder(else_body_block))

            for i in range(parse_child_count, ctx.getChildCount()): 
                if ctx.getChild(i).getText() == "}":
                    parse_child_count = i + 1
                    break

                if isinstance(ctx.getChild(i), CParser.StatementContext):
                    self.visit(ctx.getChild(i))

            self.Builders[-1].branch(end_block)  # 跳转到最终结束块


        # 结束块
        self.Blocks.pop()
        self.Builders.pop()
        self.Blocks.append(end_block)
        self.Builders.append(ir.IRBuilder(end_block))

        self.m_symblol_table.QuitScope()

        return

        


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
        
        # ! 注意eval的返回形式
        condition_result = self.visit(ctx.getChild(2))
        self.Builders[-1].cbranch(condition_result, while_statm_body, while_statm_end)

        self.Blocks.pop()
        self.Builders.pop()
        self.Blocks.append(while_statm_body)
        self.Builders.append(ir.IRBuilder(while_statm_body))
        
        for i in range(ctx.getChildCount()): 
            if isinstance(ctx.getChild(i), CParser.StatementContext): 
                self.visit(ctx.getChild(i)) 

        #执行body后重新判断condition
        self.Builders[-1].branch(while_statm_condition)

        #结束while循环
        self.Blocks.pop()
        self.Builders.pop()
        self.Blocks.append(while_statm_end)
        self.Builders.append(ir.IRBuilder(while_statm_end))
        self.m_symblol_table.QuitScope()
        
        return


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
        """
        # ! 假设三个语句都存在
        self.m_symblol_table.EnterScope() 
        

        
        llvmBuiler = self.Builders[-1]
        condition_block = llvmBuiler.append_basic_block()
        for_body_block = llvmBuiler.append_basic_block()
        end_block = llvmBuiler.append_basic_block()


        # 原block
        
        self.visit(ctx.getChild(2))
        llvmBuiler.branch(condition_block)

        # condition block
        self.Blocks.pop()
        self.Builders.pop()
        self.Blocks.append(condition_block)
        self.Builders.append(ir.IRBuilder(condition_block))
        llvmBuiler = self.Builders[-1]

        cond_result = self.visit(ctx.getChild(4))
        llvmBuiler.cbranch(cond_result, for_body_block, end_block)


        # for body block
        self.Blocks.pop()
        self.Builders.pop()
        self.Blocks.append(for_body_block)
        self.Builders.append(ir.IRBuilder(for_body_block))
        llvmBuiler = self.Builders[-1]

        for i in range(9, ctx.getChildCount()):  # 注意只处理if里面的statement
            if isinstance(ctx.getChild(i), CParser.StatementContext):
                self.visit(ctx.getChild(i))
        self.visit(ctx.getChild(6))
        llvmBuiler.branch(condition_block)

        # end block
        self.Blocks.pop()
        self.Builders.pop()
        self.Blocks.append(end_block)
        self.Builders.append(ir.IRBuilder(end_block))


        self.m_symblol_table.QuitScope()
        return 


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
        这里的语法规则和eval_expr的语法规则可能稍微有点重复了 具体内容类似
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
            return { 
                'value': ir.Constant(int32_t, int(ctx.getText())), 
                'meta': ExprType.CONST_EXPR
                } 
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
            ir_string_ptr = self.Builders[-1].bitcast(ir_string, int8_t.as_pointer())
            return { 
                'value': ir_string_ptr, 
                'meta': ExprType.CONST_EXPR
            }
        elif const_type == CLexer.FLOAT: 
            return { 
                'value': ir.Constant(float_t, float(ctx.getText())), 
                'meta': ExprType.CONST_EXPR
            }
        elif const_type == CLexer.CHAR: 
            return {
                'value': ir.Constant(int8_t, ctx.getText()[0]), 
                'meta': ExprType.CONST_EXPR
            }
        elif const_type == CLexer.ESCAPE_CHAR: 
            return { 
                'value': ir.Constant(int8_t, ctx.getText()[0]), 
                'meta': ExprType.CONST_EXPR
            }
        else: 
            raise SemanticError(msg="! Unexpected error when analizing const_val ")


    # Visit a parse tree produced by CParser#eval_expr.
    def visitEval_expr(self, ctx:CParser.Eval_exprContext):
        print("---- VISIT Eval_expr ----") 
        """
        具值表达式类型
        """
        if ctx.getChildCount() == 1:  # 如果是常量值或变量值
            child = ctx.getChild(0)
            if isinstance(child, CParser.Const_valContext): # 如果是常量值
                return self.visit(child)
            elif child.getSymbol().type == CLexer.ID: # 如果是变量值
                llvmBuiler = self.Builders[-1]
                var_id = child.getText()
                if self.m_symblol_table.exist(var_id): 
                    llvmVar = self.m_symblol_table.GetItem(var_id)
                else: 
                    raise SemanticError(msg=f"variable Undefined {var_id}", ctx=ctx)
                return { 
                    'value': llvmVar['name'], 
                    'meta': ExprType.ID_EXPR
                }
            else: 
                raise SemanticError(msg=f"Unexpected error when trying to evaluate expr {child.getText()}", ctx=ctx)

        if isinstance(ctx.getChild(0), CParser.Eval_exprContext): # 如果以表达式开头 
            if ctx.getChildCount() == 2: # 只有两个元素 说明是以表达式开头的自增或自减
                """eval_expr SELF_INC       eval_expr SELF_DEC   
                """
                return_set = self.visit(ctx.getChild(0))
                if return_set['meta'] != ExprType.ID_EXPR and return_set['meta'] != ExprType.ARRAY_ITEM_EXPR:
                    raise SemanticError(msg=f"Only ID or Array item can be inc. or dec. {ctx.getChild(0).getText()} Can not")
                return_value = return_set['value']
                llvmBuiler = self.Builders[-1]
                llvmValue = llvmBuiler.load(return_value)
                operator = ctx.getChild(1).getSymbol().type
                if operator == CLexer.SELF_INC: 
                    llvmNewValue = llvmBuiler.add(llvmValue, ir.Constant(int32_t, 1))
                elif operator == CLexer.SELF_DEC: 
                    llvmNewValue = llvmBuiler.sub(llvmValue, ir.Constant(int32_t, 1))
                else: 
                    raise SemanticError(msg=f"Undefined operator {operator}", ctx=ctx)
                llvmBuiler.store(llvmNewValue, return_value)
                return { 
                    'value': ir.Constant(return_value.pointee, llvmValue), 
                    'meta': ExprType.CONST_EXPR
                }
            

            if isinstance(ctx.getChild(2), CParser.Eval_exprContext): # 如果是二元表达式
                return_set1 = self.visit(ctx.getChild(0))
                return_set2 = self.visit(ctx.getChild(2))

                operator = ctx.getChild(1).getSymbol().type
                llvmBuiler = self.Builders[-1]
                var1 = return_set1['value']
                var2 = return_set2['value']
                if return_set1['meta'] == ExprType.CONST_EXPR:
                    val1 = var1
                else: 
                    val1 = llvmBuiler.load(var1)
                if return_set2['meta'] == ExprType.CONST_EXPR: 
                    val2 = var2
                else: 
                    val2 = llvmBuiler.load(var2)

                if operator == CLexer.MULTIPLY: 
                    # TODO: 测试文件中暂时涉及不到乘法表达式
                    return None
                elif operator == CLexer.DIVIDE: 
                    # TODO: 测试文件中暂时涉及不到除法表达式
                    return None
                elif operator == CLexer.MODULO:
                    # TODO: 测试文件中暂时涉及不到取模表达式
                    return None
                elif operator == CLexer.PLUS:
                    return {
                        'value': llvmBuiler.add(val1, val2), 
                        'meta': ExprType.CONST_EXPR
                    }
                elif operator == CLexer.MINUS:
                    return { 
                        'value': llvmBuiler.sub(val1, val2), 
                        'meta': ExprType.CONST_EXPR
                    }
                elif operator == CLexer.SHL:
                    # TODO: 测试文件中暂时涉及不到移位表达式
                    return None
                elif operator == CLexer.SHR: 
                    # TODO: 测试文件中暂时涉及不到移位表达式
                    return None
                elif operator == CLexer.GREATER or operator == CLexer.GREATER_EQUAL or operator == CLexer.LESS \
                    or operator == CLexer.LESS_EQUAL or operator == CLexer.EQUAL or operator == CLexer.NOT_EQUAL:
                    return { 
                        'value': llvmBuiler.icmp_signed(ctx.getChild(1).getText(), val1, val2), 
                        'meta': ExprType.CONST_EXPR
                    }
                elif operator == CLexer.OP_AND: 
                    # TODO: 测试文件中暂时涉及不到位级操作
                    return None
                elif operator == CLexer.OP_XOR: 
                    # TODO: 测试文件中暂时涉及不到位级操作
                    return None
                elif operator == CLexer.OP_OR: 
                    # TODO: 测试文件中暂时涉及不到位级操作
                    return None
                elif operator == CLexer.AND:
                    # TODO: 测试文件中暂时涉及不到逻辑操作
                    return None
                elif operator == CLexer.OR: 
                    # TODO: 测试文件中暂时涉及不到逻辑操作 
                    return None 
                elif operator == CLexer.ASSIGN: 
                    if return_set1['meta'] != ExprType.ID_EXPR and return_set1['meta'] != ExprType.ARRAY_ITEM_EXPR: 
                        raise SemanticError(msg=f"assigned object must be a left value, {ctx.getChild(0).getText()} is not.", ctx=ctx)
                    else: 
                        llvmBuiler.store(ir.Constant(var2.pointee, val2), var1)
                        return {
                            'value': ir.Constant(var2.pointee, var2), 
                            'meta': ExprType.CONST_EXPR
                        }
                else: 
                    raise SemanticError(msg=f"Undefined operator {operator}", ctx=ctx)
            else:
                raise SemanticError(msg=f"Unexpected error for eval_expr ", ctx=ctx)
        else: # 如果不以表达式开头
            mark = ctx.getChild(0).getSymbol().type
            if mark == CLexer.ID: 
                var_id = ctx.getChild(0).getText()
                type_mark = ctx.getChild(1).getText()
                if type_mark == "[": # 说明这一个表达式访问的是数组的值
                    return_set = self.visit(ctx.getChild(2))
                    return_value = return_set['value']
                    llvmBuiler = self.Builders[-1]
                    if return_set['meta'] == ExprType.CONST_EXPR: 
                        index_value = return_value
                    else: 
                        index_value = llvmBuiler.load(return_value)
                    if self.m_symblol_table.exist(var_id):
                        llvmVar = self.m_symblol_table.GetItem(var_id)
                        llvmvalue = llvmBuiler.gep(llvmVar['name'], [ir.Constant(int32_t, 0), index_value])
                        return {
                            'value': llvmvalue, 
                            'meta': ExprType.ARRAY_ITEM_EXPR, 
                            } 
                    else: 
                        raise SemanticError(msg=f"undefined array {var_id}", ctx=ctx)
                elif type_mark == "(": # 说明这是一个函数调用语句
                    pass 
                else: 
                    raise SemanticError(msg=f"Undefined error type {type_mark} in expr", ctx=ctx)
            elif mark == CLexer.SELF_INC:
                # TODO 测试之外
                return None
            elif mark == CLexer.SELF_DEC: 
                # TODO 测试之外
                return None
            elif mark == CLexer.NOT: 
                # TODO 测试之外
                return None
            elif mark == CLexer.MULTIPLY: 
                return_set = self.visit(ctx.getChild(1))
                if return_set['meta'] != ExprType.ID_EXPR: 
                    raise SemanticError(msg=f"only id can be dereferenced, {ctx.getChild(1).getText()} can not", ctx=ctx)
                else: 
                    llvmBuiler = self.Builders[-1]
                    ptr =  llvmBuiler.load(return_set['value'])
                    return { 
                        'value': ptr, 
                        'meta': ExprType.ID_EXPR
                    }
            elif mark == CLexer.OP_AND: 
                return_set = self.visit(ctx.getChild(1))
                if return_set['meta'] == ExprType.CONST_EXPR: 
                    raise SemanticError(msg=f"Const value {ctx.getChild(1).getText()} can not get an address", ctx=ctx)
                return {
                    'value': return_set['value'], 
                    'meta': ExprType.CONST_EXPR
                }
            elif mark == CLexer.SIZEOF: 
                # TODO 增加对于sizeof函数的支持
                pass
            elif mark == CLexer.LPAREN: 
                mark_right = ctx.getChild(2).getSymbol().type
                if mark_right == CLexer.RPAREN: 
                    return self.visit(ctx.getChild(1))
            else: 
                raise SemanticError(msg=f"undefined operator {mark}", ctx=ctx)
                


    
    def save(self, filename): 
        """
        save the IR code to file 
        """
        with open(filename, "w") as f: 
            f.write(repr(self.Module))
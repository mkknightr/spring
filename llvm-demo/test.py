from llvmlite import ir

# 创建模块
module = ir.Module()

# 设置目标三元组
module.triple = "arm64-apple-darwin"

# 创建打印 hello world 的函数
printf = ir.FunctionType(ir.IntType(32), [ir.IntType(8).as_pointer()], var_arg=True)
printf_func = ir.Function(module, printf, "printf")

def declare_print_hello():
    # 创建 print_hello 函数
    print_hello_type = ir.FunctionType(ir.VoidType(), [])
    print_hello_func = ir.Function(module, print_hello_type, "print_hello")

    # 在函数中生成 IR 指令
    block = print_hello_func.append_basic_block(name="entry")
    builder = ir.IRBuilder(block)
    
    # 创建全局字符串常量
    fmt_str = ir.GlobalVariable(module, ir.ArrayType(ir.IntType(8), len("Hello, World!\n")), name="fmt_str")
    fmt_str.linkage = 'internal'
    fmt_str.global_constant = True
    fmt_str.initializer = ir.Constant(ir.ArrayType(ir.IntType(8), len("Hello, World!\n")),
                                     bytearray("Hello, World!\n", "utf-8"))
    
    # 使用 printf 调用打印字符串
    builder.call(printf_func, [fmt_str.gep((ir.Constant(ir.IntType(32), 0), ir.Constant(ir.IntType(32), 0)))])
    builder.ret_void()

declare_print_hello()

# 创建主函数
main_type = ir.FunctionType(ir.IntType(32), [])
main_func = ir.Function(module, main_type, name="main")

# 创建主函数的基本块
entry_block = main_func.append_basic_block(name="entry")

# 进入主函数的基本块
builder = ir.IRBuilder(entry_block)

# 调用 print_hello 函数
builder.call(module.get_global("print_hello"), [])

# 返回主函数的值
builder.ret(ir.Constant(ir.IntType(32), 0))

# 保存 LLVM IR 代码到文件
with open("test.ll", "w") as file:
    file.write(str(module))

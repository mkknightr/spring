from llvmlite import ir

def create_swap_function(module):
    # 定义 swap 函数的类型：无返回值，两个32位整数指针参数
    swap_func_type = ir.FunctionType(ir.VoidType(), [ir.IntType(32).as_pointer(), ir.IntType(32).as_pointer()])

    # 在模块中创建 swap 函数
    swap_func = ir.Function(module, swap_func_type, name="swap")

    # 创建基本块
    block = swap_func.append_basic_block(name="entry")
    builder = ir.IRBuilder(block)

    # 获取函数参数
    a_ptr, b_ptr = swap_func.args

    # 加载指针指向的值
    a_val = builder.load(a_ptr, name="a_val")
    b_val = builder.load(b_ptr, name="b_val")

    # 交换操作
    temp = builder.alloca(ir.IntType(32), name="temp")
    builder.store(a_val, temp)
    builder.store(b_val, a_ptr)
    temp_val = builder.load(temp, "temp_val")
    builder.store(temp_val, b_ptr)

    # 完成函数
    builder.ret_void()


def create_for_chunk(module : ir.Module):
    
    printf = module.get_global('printf')

    # 定义 printArray 函数
    print_array_type = ir.FunctionType(ir.VoidType(), [ir.IntType(32).as_pointer(), ir.IntType(32)])
    print_array_func = ir.Function(module, print_array_type, name="printArray")
    arr, size = print_array_func.args



    block = print_array_func.append_basic_block(name="entry")
    builder = ir.IRBuilder(block)

    # 初始化循环变量 i
    i = builder.alloca(ir.IntType(32), name="i")
    builder.store(ir.Constant(ir.IntType(32), 0), i)
    
    # 循环条件
    loop_cond = builder.append_basic_block(name="loop_cond")
    builder.branch(loop_cond)
    builder.position_at_end(loop_cond)

    i_val = builder.load(i, name="i_val")
    cond = builder.icmp_signed('<', i_val, size, name="cond")
    loop_body = builder.append_basic_block(name="loop_body")
    after_loop = builder.append_basic_block(name="after_loop")
    builder.cbranch(cond, loop_body, after_loop)

    
    # 循环体
    builder.position_at_end(loop_body)
    element_ptr = builder.gep(arr, [i_val], name="element_ptr")
    element = builder.load(element_ptr, name="element")
    # 假设我们已经有了一个格式化字符串 '%d '
    fmt_str = module.get_global('fmt_str')
    fmt_str_ptr = builder.bitcast(fmt_str, ir.IntType(8).as_pointer())
    builder.call(printf, [fmt_str_ptr, element])
    # 增加 i
    
    next_i_val = builder.add(i_val, ir.Constant(ir.IntType(32), 1), name="next_i_val")
    builder.store(next_i_val, i)
    builder.branch(loop_cond)

    # 循环结束后打印换行符
    builder.position_at_end(after_loop)


    builder.ret_void()
    pass
    


def main():
    module = ir.Module(name="my_module")
    module.triple = "arm64-apple-macos"
    # 声明 printf 函数
    printf_type = ir.FunctionType(ir.IntType(32), [ir.IntType(8).as_pointer()], var_arg=True)
    printf = ir.Function(module, printf_type, name="printf")

    main_type = ir.FunctionType(ir.IntType(32), [])
    main_func = ir.Function(module, main_type, name="main")

    # 创建主函数的基本块
    entry_block = main_func.append_basic_block(name="entry")

    # 进入主函数的基本块
    builder = ir.IRBuilder(entry_block)

    # 创建格式字符串并打印 c 的值
    fmt = "%d\n\0"
    fmt_str = ir.GlobalVariable(module, ir.ArrayType(ir.IntType(8), len(fmt)), name="fmt_str")
    fmt_str.linkage = 'internal'
    fmt_str.global_constant = True
    fmt_str.initializer = ir.Constant(ir.ArrayType(ir.IntType(8), len(fmt)), bytearray(fmt, "utf8"))

    # 生成 printf 调用
    fmt_str_ptr = builder.bitcast(fmt_str, ir.IntType(8).as_pointer())





    var_a = builder.alloca(ir.IntType(32), name='var_a')
    var_b = builder.alloca(ir.IntType(32), name='var_b')

    builder.store(ir.Constant(ir.IntType(32), 11451), var_a)
    builder.store(ir.Constant(ir.IntType(32), 7890), var_b)



     # 创建 swap 函数
    create_swap_function(module)

    val_a = builder.load(var_a, 'val_a')
    val_b = builder.load(var_b, 'val_b')

    builder.call(printf, [fmt_str_ptr, val_a])
    builder.call(printf, [fmt_str_ptr, val_b])

    builder.call(module.get_global('swap'), [var_a, var_b])


    

    val_a = builder.load(var_a, 'val_a')
    val_b = builder.load(var_b, 'val_b')
    builder.call(printf, [fmt_str_ptr, val_a])
    builder.call(printf, [fmt_str_ptr, val_b])




    # ? 测试printarray

    create_for_chunk(module)
    print("[created]")


    # 创建一个整数数组
    array_type = ir.ArrayType(ir.IntType(32), 5)
    arr = builder.alloca(array_type, name="arr")

    # 初始化数组元素（例如：[1, 2, 3, 4, 5]）
    for i, val in enumerate([1, 2, 3, 4, 5]):
        elem_ptr = builder.gep(arr, [ir.Constant(ir.IntType(32), 0), ir.Constant(ir.IntType(32), i)], name="elem_ptr")
        builder.store(ir.Constant(ir.IntType(32), val), elem_ptr)

    # 调用 printArray
    size = ir.Constant(ir.IntType(32), 5)
    arr_ptr = builder.bitcast(arr, ir.IntType(32).as_pointer(), name="arr_ptr")
    builder.call(module.get_global("printArray"), [arr_ptr, size])








    # 返回主函数的值
    builder.ret(ir.Constant(ir.IntType(32), 0))

    with open("swap.ll", "w") as file:
        file.write(str(module))


   
    # 打印生成的 LLVM IR
    # print(str(module))

if __name__ == "__main__":
    main()

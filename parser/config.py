class Configuration: 
    """
    configurations for llvm IR generation 
    """

    LLVM_TRIPLE_MACOS = "arm64-apple-macosx"
    LLVM_TRIPLE_WINDOWS = "x86_64-pc-windows-msvc"
    LLVM_DATA_LAYOUT = "e-m:e-i64:64-f80:128-n8:16:32:64-S128"


    ERROR_UPEXPECTED = "Unexpected error encountered"


class ExprType: 
    """
    eval_type to mark in the return value of eval_expr 
    """
    CONST_EXPR = 0
    ID_EXPR = 1
    ARRAY_ITEM_EXPR = 2
    VAR_EXPR = 3
    ARRAY_POINTER = 4